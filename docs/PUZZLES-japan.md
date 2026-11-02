# Act Six: By Your Grace (Japan, spring 1830): the puzzles

<!-- MERGE-20: new in round twenty. The design is briefs/out/edo-design.md; the act is js/content/acts/edo.js (act 7); its
three legs were built by SCENES-20A, 20B and 20C, and each wrote its part below. -->

Meanwhile, in another time: Mom, Big Sister and Little Sister come through the coin door expecting the Son, and step out
onto a beach at Yui, on Suruga Bay, in the spring of 1830 (Bunsei 13, the year of the metal tiger), in their own clothes,
in a country where foreigners landing are to be seized. The act is a journey west in five legs, each its own place or
places on the map of Japan (a woodblock travel map: `art/maps/edo/`): Yui and the Satta Pass above it (a woman without a pass
cannot go west by road); a day on the ship at sea; Osaka, twelve days from Yui, at the height of the 1830 pilgrimage; the
hills north of it, by the Kyoto boat; the Akashi shore, three days' walk west; and Himeji, a day on, with the women's hall
of Engyō-ji at the foot of Mount Shosha, where women stopped because they were not allowed up the mountain, and where at
sunset a boy's voice speaks through a small door. The map takes the family only between the places of the leg they are in;
a place of another leg is drawn in, and Mom says why they are not going back (`maps.js`, a place's `leg` and `far`, the far
line said for the leg the family is in).

The rules the whole act keeps: nobody in the family lies (every option the player can pick for them is true, and the
comedy is in exactly true answers); the Japanese people speak as everyone in the game speaks, and a few of their own words
are glossed once; nothing frightening (the board is read once, the constable yawns, the warden's fright is comic); and the
hidden family under the storehouse is written with respect and warmth, never pity. Scripture is the King James text:
Psalm 139:9-10 at sea, Jeremiah 31:17 at the Osaka crossroads, Matthew 6:9 in the room underground, John 1:5 for the
grandmother, Psalm 61:1-2 at the foot of the mountain the women may not climb, Isaiah 49:15 at the small door.

<!-- MERGE-21: made bigger in round twenty-one (the design: briefs/out/edo2-design.md). The act is a journey in five legs on its
map now (Suruga; Osaka; the hills; Akashi; Himeji with Shosha), with a day at sea between the first two: twenty-one puzzles,
#21 to #41, numbered in the order they are played. The parts below: round twenty's Yui, then round twenty-one's Suruga and the
sea (SCENES-21A), Osaka and the hills' changes (SCENES-21B), round twenty's hills, the road west to the women's hall at Shosha
(SCENES-21C), and round twenty's castle. -->

**The beats** (`js/content/acts/edo.js`, act 7), in story order: `edo.arrive`, `edo.when` (#21), `edo.dressed` (#22), `edo.fed`
(#23), `edo.road` (#24: `edo.noRoad`), `edo.west` (#25), `edo.castoff` (`edo.aboard`), `edo.heading` (#26: `edo.headingCalled`),
`edo.chirp` (#27: `edo.chirped`), `edo.sail` (`edo.sailed`), `edo.alms` (#28: `edo.vouched`), `edo.heard` (#29: `edo.combGiven`),
`edo.read` (#30: `edo.sheetRead`), `edo.troupe` (#31: `edo.troupeTaken`), `edo.boat` (`edo.boated`), `edo.hidden` (#32),
`edo.trusted` (#33), `edo.mirror` (#34), `edo.walk` (`edo.walked`), `edo.ladle` (#35: `edo.ladleBack`), `edo.walk2`
(`edo.inHimeji`), `edo.supper` (#36: `edo.supperMade`), `edo.hall` (#37: `edo.hallOpen`), `edo.son` (#38: `edo.holdHands`),
`edo.night` (`edo.nightDone`), `edo.inside` (#39), `edo.up` (#40), `edo.door` (#41), and the gate `edo.end` (`edo.done`, and
`demo.done`). The stage facts each hint reads are in the act file's head comment.

Until #21 is solved the game never says the year: the map's band, its chip and the saved games show "Japan" alone (an
era's `dateAfter`, docs/DESIGN.md).

## The act at a glance

```
                  Cut-scene: Meanwhile, in another time (the beach at Yui, dawn)                    [as built]
                                           |
        +----------------------------------+-----------------------------------+
  #21 Where, And When              #22 Out Of Sight (+ O-Tami's hairpin)    #23 Kihei's Table      [as built]
        |                                  |                                   |
        |                     #24 West (the hens; the road; Nishikurasawa; the top of the pass;
        |                         a woman's pass on the Jizō, given back; Arai; not by road)      NEW (the hens as built)
        |                                  |                                   |
        |                     #25 A Captain Who Says Yes (Kihei names the ship; Gonroku; O-Masa) [as built, moved]
        +----------------------------------+
                    Cut-scene: Casting Off (the goodbyes; the ship's boat; the windlass; the sail)  NEW
                                           |
                  +------------------------+------------------------+
          #26 Etekō                                      #27 Don't Lift The Lid                     NEW, the deck
          (Big Sister: the ship's clock;                 (Little Sister, Mom: Kōta's rice; the Funadama's
           the word you don't say at sea)                 things; a penny for a coin; she chirps)  -> the COIN
                  +------------------------+------------------------+
                    Cut-scene: The Uttermost Parts (night; Psalm 139; "Eight days later" / Osaka)    [as built, edited]
                                           |
                     #28 The Dōjima Shore (no ladle; Mom takes the paddle; "My helpers.")           NEW, Osaka
                                           |
                  +------------------------+------------------------+
          #29 What The Road God Said                     #30 Berlin Blue
          (Mom: the crossroads comb; the yomiuri;        (Big Sister: the print shop; the marks;
           "a boy's voice at Shosha")  -> the COMB        the sheet read aloud: the lock no comb opens)
                  |                                                 |
          #31 Three To A Puppet (the girls in black at the Inari theatre; the boy runs home)
                  +------------------------+------------------------+
                    Cut-scene: The Kyoto Boat (Hachikenya; the haulers; "won't ya stuff some rice?";
                    the ferry; north; the rain)                                                      NEW
                                           |
                     #32 Under The Cedars / #33 Our Father / #34 Charcoal, And A Kind Child          [as built: old #25-#27]
                                           |    -> the mirror, the trowel, the castle's two stories
                    Card: Three days later / Akashi ("Everybody else was going the OTHER way.")     [edited]
                                           |
                     #35 The Ladle (Little Sister wades; the octopus; the crab; O-Fusa's slip;
                         O-Sato's news: "it opens to what a ship gives its lady")                    NEW, Akashi
                                           |
                    Card: The next day / Himeji                                                       NEW
                                           |
                     #36 Supper For A Voice (O-Kiku's first day; O-Shizu's map; Mom's rice balls)   NEW, Himeji town
                                           |
                     #37 What A Ship Gives Its Lady (the women's hall: the pin, the coin, the comb,
                         three hands at once; the lock chirps)                                        NEW, THE TEMPLE
                                           |
                     #38 A Small Door At Sunset (the Son; more light; a rice ball for Rome; "Hold hands.") NEW
                                           |
                    Cut-scene: Mind The Fire (the walk back; the clappers, gate to gate); "The next day" NEW
                                           |
                     #39 Eight At The Gate / #40 A Light That Needs No Fire / #41 The Lady Of The Keep  [as built: old #28-#30]
                                           |
                    Cut-scene: Hold Hands -> "to be continued" -> the title (edo.done, demo.done)      [as built]
```

## Act Six, the first leg: Yui, on Suruga Bay (#21 to #23, and round twenty's #24), as round twenty built it

<!-- MERGE-21: round twenty's #24 "West" is now two puzzles: #24 West (the hens, the road over the Satta Pass, the woman's pass, Arai) and
#25 A Captain Who Says Yes (Kihei names the ship after the road; Gonroku; O-Masa); the voyage is Casting Off, the deck (#26, #27)
and The Uttermost Parts. This section stands as round twenty built Yui; the next part has round twenty-one's changes. -->

<!-- SCENES-20A: new in round twenty, for MERGE-20's docs/PUZZLES-japan.md (in the manner of the Office's part of
docs/PUZZLES-the-present.md). -->
Meanwhile, in another time: Mom, Big Sister and Little Sister come through the coin door expecting the Son, and step out
onto a beach in Japan in the spring of 1830, in their own clothes, in a country where foreigners landing are to be seized.
The first leg of the act is one village on the Tōkaidō under the Satta pass, Yui, and one shop in it, Kihei's: four
puzzles (#21 to #24), the arrival and the voyage. The design is `briefs/out/edo-design.md`, sections 5 and 7; the lines are
`js/content/lines/edo-a.en.js` and the talks are trees in `js/content/talk/edo-a.js` (WRITE-20A's; their writer's `ids.md`
says when each line is said); the act is `js/content/acts/edo.js` (act 7); the two scenes are
`js/content/scenes/edo-village.js` and `edo-fishshop.js`, with what they share in `edo-yui.js` beside them (and what the
whole act shares in MERGE-20's `edo-common.js`); the two cut-scenes are `js/content/cutscenes/edo-arrive.js` and
`edo-sail.js`. Play it: `index.html?scene=edo-village&lead=mom&flags=office.done` (the "Meanwhile" card and the arrival
play first; add `,edo.arrived` to start on the beach), or `index.html?scene=edo-fishshop&lead=mom&flags=edo.arrived,edo.clerkPassed`.
What follows is the leg as the game plays it. Where the builder chose something the design left open, or staged it
otherwise, the card says so.

### The three, together

The family is the team: three portraits at the top left, Mom played first (Going Down's hand-on: `EDO_HANDON`), Big
Sister and Little Sister beside her in both scenes (each scene's `party`), and the player can play any of them at any
time, where she stands. They are always together in Yui; the shop and the village are next door to each other (a walk
through the noren). The map is the act's (`maps.js` `edo`, PAINT-20B's woodblock road map): from Yui nothing else is a
place to go yet, and the voyage is a journey on it, not a way.

| | What only she can do here | What she will not do |
| --- | --- | --- |
| **Mom** | Ask a grown-up the right question: O-Masa (#24). Hold a baby who has not slept in three days, and hum her to sleep (#22). Say thank you properly. | Lie. Not to the clerk, not to anybody: she says true things and leaves things out ("A small true piece is still true. A large false one isn't. Keep them small."). |
| **Big Sister** | Read a year out of a red hood, a box of coins and a print (#21); know mackerel and Prussian blue; give the act its name ("It means 'thanks to you'. Or 'by your grace'."). | Read anything at all here ("I used to be able to read."): she reads people instead. Touch a god-shelf, or another person's money. |
| **Little Sister** | Ask a nine-year-old what the board says, and learn "arigatō" from him; see the hens face west (#24); fit under the floor after a cat (#23); keep her yellow boots (#22). | Give up her boots, her egg or her three pennies (handed to her mother or sister, they come straight back: "It's warm. It's MINE to keep warm."). |

**The clothes.** They arrive in their own clothes (the first villager to see them drops her basket). O-Tami's old travel
kimonos (#22) are kept in the save (`g.dress`): from then on the three are in them for the rest of the act, the sedge hats
on their heads outdoors (`edo`) and down their backs indoors (`edo-hatback`); Little Sister keeps her yellow boots in
every outfit. Once they are dressed, the act's stock replies see them so (`edo-common.js` `stockFor`: Mom on Big Sister,
"My eldest, in borrowed indigo, reading faces because she can't read signs."). Mom with the baby in her arms is an outfit of her own clothes made at run
time (`edo-yui.js`: `mom-baby`), since the lullaby comes before the kimonos; the three sitting on the step of the raised
room to eat are seated pages made the same way (`<outfit>-step`, 45 cm, PAINT-20B's seats).

**The sounds.** The sea on the shingle (the `waves` loop: full on the beach, half in the shop, through its open front),
gulls now and then, the noren flapping as they go in and out, Kihei's press (a soft knock of wood on wood), a rooster up
the beach at the arrival, the door in time closing behind them like a breath let go, Mom's hum (four bars of a tune of her
own: `lullaby`), the ship's timbers creaking on the voyage. The music is the act's own (`edo`).

### Puzzle structure

```
                    Cut-scene: Meanwhile, in another time (the beach at Yui; the act's card, no year on it)
                                              |
            +---------------------------------+----------------------------------+
            |                                 |                                  |
  #21 Where, And When              #22 Out Of Sight                    #23 Kihei's Table
  (Big Sister; the shop)           (Mom; the shop and the street)      (any of the three; the shop)
  the red: O-Tami (a metal         the clerk's first pass (the shop);  "...Sit." The price that is not a
  tiger); the coins: the money     the baby: Mom hums her to sleep;    price; the press, the step, the
  box; the blue: the print         the kimonos from the chest; the     grace, the bow, the word, Okage-
  -> the sum: 1830, the act's      clerk, dressed: "travellers,        sama de; the cat and the mackerel;
     card with the year            three, going west"                  the box for the road
            |                                 +----------------------------------+
            |                                                  |
            |                       #24 West (Little Sister, then Mom; the street and the beach)
            |                         the hens face west; Kihei names the ship; Gonroku: no women aboard
            |                         (every argument fails); his wife, asked properly: the passage
            |                                                  |
            +-------------------------------->  the ship, at first light: the goodbyes (the year must be
                                                worked out first: Big Sister will not sail out of a year
                                                she cannot name)
                                                               |
                         Cut-scene: The Uttermost Parts (the ship by night; Psalm 139; Osaka; the hills)
```

Goal of the leg: **work out where and when they are, stay out of sight, eat, and find a way west.** #21, #22 and #23 are
chains A, B and C, in any order (#22's clerk needs its kimonos, and its kimonos the baby asleep); #24 needs #22 and #23
(O-Masa will take a question only from someone dressed, fed and passed by the clerk). The beats (`acts/edo.js`, act 7),
each with its fact: `edo.arrive` (the cut-scene, `edo.arrived`; it needs `office.done`), `edo.when` (#21), `edo.dressed`
(#22), `edo.fed` (#23), `edo.west` (#24, the first leg's gate) and `edo.sail` (the voyage, `edo.sailed`). The facts the
staged hints read are the scenes': `edo.clue.red`, `edo.clue.coins`, `edo.clue.blue` (#21); `edo.clerkPassed`,
`edo.babySleeps`, `edo.clothes` (#22); `edo.kiheiMet`, `edo.pennyShown` (#23); `edo.hensWest`, `edo.kiheiWest`,
`edo.gonrokuNo`, `edo.gonrokuWife` (#24). Every hint is each of the three's: the one whose job it is says what to try, the
others whose job it is ("My sister does the when. I do the chickens. We have a SYSTEM.").

### Location layout

Two places, one painting each, both of the same morning and the same village: the street outside, and the shop's inside
with the street in its open front.

```
YUI (edo-village): the beach and the village street along the Tokaido, morning; one floor (the street a little up a sand slope)
+-----------------------------------------------------------------------------------------------------+
|                         FUJI, white and enormous, across SURUGA BAY        the PASS (Satta), and the   |
|                                                                            SHRINE PATH with its CHERRY |
|  gulls        Gonroku's SHIP at anchor, far out                            (petals falling)            |
|  ~~~~~~~~ the BAY (waves coming in) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~   the ROOFS (stones on shingles),      |
|  the TENDER    GONROKU at the water's edge          the NOTICE BOARD     SMOKE from a kitchen, the WELL     |
|  the NET RACKS (nets drying)   O-MASA at the nets   and SANKICHI         +---------------------------+   |
|  the big BOAT on its props,    the NET-MENDER       TOKUZO (the clerk,   | KIHEI'S SHOP: the NOREN   |   |
|  the GAP under it              (sitting)            after the first      | (the way in); KIHEI out   |   |
|                                the VILLAGE WOMAN     pass)               | front in the morning      |   |
|  the SAND        the ring WHERE THE DOOR WAS (arrive)       the ROAD     +---------------------------+   |
|                                                                          the FENCE, the HEN YARD (five |
|                                                                          hens, every one facing west)  |
+-----------------------------------------------------------------------------------------------------+

KIHEI'S SHOP (edo-fishshop): inside, an earth floor open to the street; the raised room of mats at the right
+-----------------------------------------------------------------------------------------------------+
|  DRIED FISH, SEDGE HATS        the open front: the STREET, the beach, the bay (waves), FUJI; the NOREN |
|  STRAW SANDALS hung for sale   (Tokuzo goes past outside, the first time)     the GOD-SHELF, high      |
|  the CUTTING BOARD, the TUBS of fish (one jumps)    the PRINT of Fuji (on the post)                   |
|  KIHEI at his board            the earth floor           the MONEY BOX (strings of square-holed coins) |
|  the SUSHI BOX on its stand                              | the STEP (the raised room's edge, where     |
|  O-TAMI (the baby on her back)  THE CAT (her place)      | guests sit); the GAP under the floor;       |
|  the HEARTH and its pot (steam)                          | the CHEST; the BASKET (the baby, asleep)     |
|  (the way out: YUI, through the open front)              | the mats (nobody's floor)                    |
+-----------------------------------------------------------------------------------------------------+
```

The village's way into the shop is its noren ("Go into Kihei's shop"); the shop's way out is its open front ("Go out to
Yui"). The ship is reached only by the voyage.

### Cut-scenes and puzzles

```
Cut-Scene: Meanwhile, in another time        (opens the act)
```
After Going Down's card (LAMPLIGHTER, "to be continued"), the card "Meanwhile" / "in another time" on black (Going Down's,
when it hands the game on; the village's own when it plays the cut-scene for a game that has not had it). The tunnel, the
years flying past, and out: the beach at Yui in the morning, the bay, the boats, and across the water Fuji. On the sand by
the boats the paint ripples into a door in time, tall and narrow as a doorway (ENGINE-20's portal); the three step out of
it one after another and walk to their places, and it closes behind them with a sound like a breath let go. They count
off: "Places, girls." "Here." "HERE. ...Where's here?" Little Sister, first, looking at the mountain: "This isn't ROME."
Big Sister: "That's Mount Fuji." "...Is he here?" Mom, after a moment: "No, sweetheart. Not here." She looks at the closed
air where the door was: "Then we keep going. That's all we can do, and we can do that." A gull. A rooster somewhere up the
beach. Little Sister: "A rooster. ...Okay. I can work with a rooster." The village woman with the basket on her back has
seen them: her hands go to her face, the basket goes down on the sand (radishes, a cabbage) and she says, with great
dignity, "...I'll come back for the basket," and goes up the street. Mom: "We've made an impression, girls. Let's make a
better one." The act's card over the beach: "Act Six: By Your Grace", and nothing under it (when they are is #21: the era's
card, "Japan, spring 1830", is never shown on arrival). Play as Mom. The pockets are as Act Four left them (the coin to Big
Sister if nobody had it; Little Sister's egg, and her pink flashlight given back to her). Skipped, the cut-scene lands in
the same place: the three on their marks, the basket on the sand, the woman gone (she is back with it the next time the
village is built).

```
Puzzle #21: Where, And When        (Act Six · Lead: Big Sister · the shop)        chain A
Needs:        the arrival
Setup:        Japan is plain. When is not: Big Sister cannot read a single character on any sign, and it is the worst
              morning of her life.
Wrong tries:  The notice board                -> "I can't read it. I can't read ANY of it." Asked of Sankichi: "You're
                                                 staring at the board. Can you read?" "...I used to be able to read."
              The tubs of fish                -> "Saba. That's mackerel. I know mackerel and wasabi, and that's ALL I know."
              The god-shelf                   -> "That's a shelf for a god. I'm not going to touch it, and I'll tell you why."
                                                 "Because it isn't mine, and because I can't read what it says."
              Dad's pencil on the sticky note, -> "I'd write the year down if I had one. I have a pencil and a feeling."
              before the year
              Sankichi, asked the year        -> "The thirteenth year of Bunsei. Everybody knows that." "...I don't know what
                                                 that is. I'm writing it down anyway. Bunsei thirteen." (true, and no help,
                                                 until it is: it goes on the act's card)
Clues:        Any order, each Big Sister's fact, said as it comes in:
              The red    O-Tami, asked why her husband wears red (by any of the three): "He's sixty. It's a tiger year, the
                         metal one, the same as the year he was born." ... Big Sister: "Sixty years, and the same sign comes
                         round. A metal tiger. I can work with that." (`edo.clue.red`; Kihei himself only says "Ask my wife.")
              The coins  the money box, looked at by any of the three: Big Sister, "Kan'ei Tsūhō. The label said Edo period:
                         sixteen-thirties to eighteen-sixties." and, once the red is in, "So: a tiger year, in the Edo
                         period. We are narrowing it down. Slowly." (`edo.clue.coins`)
              The blue   the print of Fuji on the post, looked at: Kihei, "Everybody in Edo wants pictures of the mountain this
                         year. In that new blue." Big Sister: "New. He said new. That's Prussian blue. Their printers only just
                         got it." (`edo.clue.blue`; or Kihei asked about it in his talk: "A pedlar...")
Solution:     The moment the third is in, Big Sister counts on her fingers and works it out aloud: "A metal tiger. They come
              round every sixty years. The last one was 2010." "Take away sixty. And sixty. And sixty: 1830." "Edo coins: yes.
              The new blue: yes. 1830." Little Sister: "Is 1830 good?" "It's a year. A year is just a year until you know what
              happens in it." Mom: "Then let's find out politely." The act's card again, with her line under it: "Spring,
              1830. Bunsei thirteen. The year of the metal tiger."
Gives:        `edo.when`. Dad's pencil on the sticky note now writes the sum down (whoever holds both, item on item:
              ENGINE's new `combine`, a scene's): Big Sister "2010, less sixty, less sixty, less sixty: 1830. On paper now.
              Now it's a fact."; Mom "Your father's pencil, a sticky note and a date. He'd be pleased with all three.";
              Little Sister "I wrote 1830. It's the best 1830 anybody's ever written. Look at the 8."
Notes:        The year is the voyage's gate too (SCENES-20A): with the passage agreed and the year not yet named, the ship
              is refused by Big Sister ("Not yet. I won't sail out of a year I can't name. The year first, then the sea.")
              The clues are all in Yui, and nobody comes back here.
```

```
Puzzle #22: Out Of Sight        (Act Six · Lead: Mom · the shop and the street)        chain B
Needs:        the arrival
Setup:        Three women in strange clothes on a post-town street, the morning after strangers were seen on the beach at
              dawn. The notice board at the village entrance, and Sankichi beside it, who can read.
Step 1:       The board. Little Sister asks Sankichi what it says, and he reads it, under its close-up (a board of dense
              columns under a little roof): "That one's the oldest. Older than Grandfather. It says 'Ordinance' at the top."
              "The Kirishitan sect is forbidden, like always. Tell on one and you get silver." "Five hundred pieces for a
              padre. A hundred for anyone who prays to their god." "Teacher says nobody's seen a padre in nearly two hundred
              years." "The silver's still up there, though." Mom: "Then we pray quietly here." Little Sister: "That's MEAN."
              Mom: "It is." It is read once (`edo.boardRead`); asked again, "The others are about poison and horses. Horses
              cost more."
Step 2:       The clerk's first pass: the first time they go into Kihei's shop, O-Tami has them in behind the noren: "In. In,
              in, in. Behind the curtain, all of you, and not a word." "Why are we--" "Because she asked, sweetheart.
              Nicely, and quickly." She stands in the opening and talks weather at Tokuzō, out in the street (he peers in
              past her): "Clerk. Fine morning. The wind's gone round to the west." ... "Fish and wind. ...I'll write
              'nothing'. It's shorter." His back goes past the opening, and O-Tami turns round: the headman's paper,
              "strangers on the beach at dawn, in strange clothes"; "I don't know any strangers. I know three travellers who
              need proper clothes." "And I have a baby who hasn't slept in three days. Three. Days." Mom: "Then one thing at
              a time. Which first?" "...Ask me when I've slept." (`edo.clerkPassed`; Kihei, out front until then, comes in
              after them to his board.)
Step 3:       The baby, on O-Tami's back. Mom asks to try ("May I try with the baby? I've had three. One of them was
              worse."; or uses the baby: "May I? ...Thank you. Come here, little one."). O-Tami: "Take her. Take her with my
              blessing. Take her to Edo if she'll sleep there." "She won't take the hearth side, she won't take the street
              side, she won't--" Mom rocks her and hums (no words), and the baby is asleep in the middle of the sentence. The
              cat, too. "...What did you DO." "I hummed in the right key. She's a quarter-tone flat herself. So's my husband."
              "Don't stop humming. Don't ever leave. ...The chest. Come to the chest." Mom lays her in her basket on the mats.
              (`edo.babySleeps`)
Step 4:       The kimonos (the clothes asked for again: "She's asleep, and I'm a woman of my word. The chest. Quietly."):
              O-Tami fetches them from the chest, an armful, and hands each over as she names it: "My mother's. She wasn't
              your height. Nobody is. Arms up." (Mom in green) "Green. You've found me my own color in a drawer in another
              century." "Indigo for the reader. It was long on me." (Big Sister) "It ends at my knees." "Travellers hitch
              them up anyway. You're ahead of everybody." "Pink for the small one. And hats, all three. Heads down under
              them." "Sandals. Fifteen mon a pair and good for a day or two of road. Yours, and yours." "What about ME?"
              "Nothing small enough for you. ...Off with the yellow ones. We'll wrap your feet." "They're my BOOTS."
              "...They are. Keep them. Nobody who sees them will believe them anyway." (Little Sister in pink, her boots on)
              "Thank you. Properly, and not for the last time." "Three travellers. Go and be travellers at the clerk, before I
              change my mind." (`edo.clothes`; the hats down their backs indoors.)
Step 5:       The clerk, dressed, on his rounds in the street. He peers (very close). Every answer the player can pick is
              true: "Good morning. Forgive me. ...Forgive me. Travellers?" "We are. We're going west." "West. Good. ...From
              where, if I may?" Big Sister: "From the east." "The east. ...Yes. Most people are. I'll write 'the east'." Mom:
              "..." "It's true, Mother. Every word of it." "You are very tall." "I am." "...So you are. Well. One can't write
              'tall'. There's no box for it." "'Travellers. Three. Going west.' Nothing seen. ...Good." He bows, and goes off
              home along the street, pleased. "'From the east.' Mother. That was true." "It was, darling. That's the only
              reason you got away with it." "He didn't look at my boots ONCE. He can't see his own feet."
Wrong tries:  The clerk before the kimonos   -> O-Tami out of the shop, a hand on Mom's sleeve: "Not like that, dear. Not in
                                                that." (`edo.tokuzo.notyet`, `.notyet.2`)
              Little Sister at the clerk,    -> "The boy says everybody's looking at my BOOTS." "Then we'd better give them
              in her own clothes                something duller to look at, sweetheart. Inside."
              The clothes before the baby    -> "Clothes need two hands. I have a baby in one and this shop in the other."
                                                "Get her to sleep, and I'll dress the three of you like the lord's own daughters."
              The chest, opened              -> "I lifted the lid ONE inch. The baby lady looked at me. I put it down."
Gives:        `edo.dressed`; the three in Edo clothes for the rest of the act.
Notes:        The baby is on O-Tami's back until she sleeps (PEOPLE-20's `tami-baby`), then in her basket (SCENES-20A: two of
              the lines said "in a basket" before; changed in place). The stock replies see them dressed from the kimonos on.
```

```
Puzzle #23: Kihei's Table        (Act Six · Lead: any · the shop)        chain C
Needs:        the arrival
Setup:        They have not eaten since Nevada, and Little Sister says so. They have no money: a car key, Dad's pencil, a
              sticky note, three American pennies with no holes in them, an egg. Kihei, the first time, says one word:
              "...Sit." (out in front of his shop in the morning, or at his board).
Steps:        Mom asks the price of a fish ("For a fish. ...Sit." "We have no money that works here. I'd rather you knew."
              "I know. Sit."); Big Sister asks for the record ("The record can sit too."); Little Sister is hungry ("Sit.");
              or Little Sister's pennies (handed to him): "No hole. How do you carry it?" "In my POCKET." "Keep it in your
              pocket, then." "He gave it BACK. Nobody gives money back. I like him even more." Whichever: "Sit. Watch, if you
              like. Don't help." "I'm good at not helping. Ask my sister." He presses mackerel sushi in the wooden box,
              behind his stand, and the player watches: the rice and the fish in, the lid, the weight stone, his weight on
              it (a knock of wood on wood), the cut. Big Sister: "Rice into the box. Fish on the rice. Lid on the fish. And
              now he just... leans." Mom: "He's pressing it. Like a flower in a book, only you can eat it." "Saba. Mackerel.
              I know that one. Pressed in a box, and cut like a cake." "Fun fact: in Edo they've just started making it by
              hand, one piece at a time." Kihei: "Eat first. Money is for after. There is no after for money today." He
              carries the board of cut pieces to the step of the raised room and sets it on the mats; the three sit on the
              step. Little Sister's grace, the three with their heads down: "Thank You for the fish, and for the fish man,
              and for his wife," "and for the baby who's asleep now. Please keep her asleep. Amen." Kihei and O-Tami wait,
              puzzled and polite, and then turn and bow to the god-shelf, and say nothing. "Eat, girls. Slowly. ...All
              right. Not slowly." While they eat: "I'm eating it with my HANDS. The fish man does too. So it's manners."
              "One at a time, sweetheart. They're not going anywhere. ...They are. Slow down." "Fish on rice in SQUARES.
              Sour. I like sour. I had THREE." "Pressed mackerel sushi. Sour, salt, cold fish. I may never eat anything
              else." "I took another. He nodded. I have never been so glad of a nod." "Pressed mackerel on rice, cut square.
              Given, not sold. Eat it like a gift." Then Little Sister: "Arigatō." (if Sankichi has given her the word: Kihei's
              face does something nobody has seen it do; O-Tami: "...Husband. Your face." "It does that."; without it, "Thank
              you, fish man. I'm going to learn how to say it properly. Watch me.") Mom: "Thank you. You've fed three
              strangers who can't pay you, and asked them nothing." Kihei: "Okage-sama de." Big Sister: "It means 'thanks to
              you'. Or 'by your grace'." "It's what you say when something good happened and it wasn't only you." The cat
              has got up on the cutting board behind the stand, and comes down with a mackerel in her mouth: "The cat has a
              mackerel." "The cat always has a mackerel." "I FIT." The cat dashes under the raised floor; Little Sister gets
              up off the step and goes in after her on hands and knees, and comes back: "Got it. ...And a cobweb. The
              cobweb's free." "...Nobody has ever got one back from that cat." "There. We've paid in fish." "In MY fish."
              "After. As you said." O-Tami wraps the rest in a bamboo leaf: "The rest goes with you. Don't argue. I'm holding
              a baby, and I'll win." and puts it in the hands of whoever is played (the `sushibox`); they get up off the
              step. With the word: "Arigatō. ...I said it to her too. It's for EVERYBODY now."
Gives:        `edo.fed`, `edo.boxGiven`, `edo.catGone`; the box of sushi, eaten on the ship.
Notes:        The scene is a kindness, not a lock: the sushi is offered before anyone has done anything, whoever asks. The
              food lines (`edo.shop.food.*`) are said at the table, while they eat (SCENES-20A: the player has no hand free
              during the meal, which is one talk with the staging between its nodes). The egg shown to Kihei: "An egg. You
              have an egg and I have fish. Keep your egg." "I wasn't GIVING it. I was showing. It's a Nevada egg. It's been
              places." Little Sister sits on the step any time ("I sat. Nobody said no. ...The cat sat too. We're a club.").
              After the meal the cat stays under the floor with the other fish ("Bye, cat. Keep the OTHER fish.").
```

```
Puzzle #24: West        (Act Six · Lead: Little Sister, then Mom · the street and the beach)        THE FIRST LEG'S GATE
Needs:        #22 and #23
Setup:        The door they came through is gone ("I knocked on the air. Nobody answered. The air's being RUDE."). Where is
              another?
Step 1:       Little Sister at the hen yard: the five hens, every one standing at the fence facing west along the coast:
              "They're all looking the same way. Every single one. That way." "Chickens KNOW." Big Sister: "West is a very
              large direction." Mom: "Then we'll ask someone who knows the roads. The fish man sees everything go by."
              (`edo.hensWest`)
Step 2:       Kihei, asked about west: "The road over the pass is the Tōkaidō. Kyoto. Osaka. The Inland Sea past that." "A
              long way on sandals. Shorter by sea." "My sister's husband's ship is in the bay. Osaka, morning tide. Dried
              bonito." "He won't take you. ...Ask anyway. Ask the right one." (`edo.kiheiWest`)
Step 3:       Gonroku, by his boat at the water's edge: "Asked. No." "The Funadama's the ship's own lady. She doesn't care
              for other women aboard." Every argument fails, in weather (Big Sister's hair, Little Sister's luck, Mom's
              quiet, the men, the stern): "Hens don't sail. ...Wind's freshening. No." The clue: "Ask my wife. She knows what
              everybody likes. At the nets. Mind how you ask." (`edo.gonrokuNo`, `edo.gonrokuWife`)
Step 4:       O-Masa, at the net racks. A favour is the wrong foot ("That's a favour. Favours I give my brother. Questions
              I'll take from anybody."); a question before they are ready gets her verdict (not dressed: "Not in that."; not
              fed: "You haven't eaten. I can hear it from here."; not past the clerk: "The clerk hasn't seen you go out.
              Him first."). Dressed, fed and written down: "Ask it." Mom: "What would the Funadama make of three women who
              sit still and have manners?" "..." "That's a question. ...Stay here. All three. Don't follow me." She puts the
              net down and goes down the beach to her husband; the family stays where it is, and hears only the end of it:
              "...The Funadama is a lady. A lady likes company with manners." Gonroku, after a long look at the sea:
              "...They sit in the stern, and they don't whistle." "I can't whistle anyway. I've been TRYING for a year."
              "The stern is the back. I know one nautical thing, and that was it." "Thank you. Both of you. We'll be no
              trouble, and very quiet." "Tide's at first light. The tide doesn't wait, and I don't argue with it."
Gives:        `edo.west`.
Step 5:       The goodbyes, when they go to the ship (Gonroku again, or the ship itself), in the street before the shop:
              Kihei and O-Tami out of it (the baby asleep on her back), Sankichi from the board. "Thank you for the clothes,
              the table, the morning. I won't forget one of them." "Go west and don't be tall at anybody. ...Come back when
              the baby can talk." "Stern. No whistling. Eat the box before it eats you." "Thank you. I learned one word today
              and lost all the others. A fair trade." Little Sister: "Bye, baby. Stay asleep. Bye, cat. Keep the OTHER
              fish." and at the hen yard, naming them: "Bye, Peck. Bye, Dot. Bye, Other Dot. Bye, Fuji. Bye, Admiral. Bye,
              Jumpy." "The hens don't have names." "They do NOW. And Jumpy's a fish. He's an honorary chicken." (If she has
              not had the word yet, Sankichi gives it to her here.) Sankichi: "Uncle Gonroku's boat? He never takes ANYBODY.
              ...Bring me back a story." "I'll bring you back TWO. Arigatō for the word."
Notes:        The lever is a person, not an argument (Mom's ability: adults listen to her, and she knows which adult to ask).
              The year must be worked out before they sail (#21: see there).
```

```
Cut-Scene: The Uttermost Parts        (the voyage)
```
The card "The Uttermost Parts", on black. The ship at night under its one great sail, the sea dark and enormous, a moon
and its road on the water, the coast a line of low lights, a lantern at the stern; the three of them dark against the
moonlit sea, the deck riding the swell. (Nobody painted a ship: the night is drawn over the stage as a picture, the three
in it as shapes.) The box, eaten at the rail, the girls on a coil of rope: "We ate the WHOLE box. On a boat. At night.
Best Tuesday ever." "It isn't Tuesday. I have no idea what it is. ...It was a very good box." Later: Big Sister asleep on
the rope and Little Sister asleep on Big Sister, and Mom at the stern rail, saying it to the sea, quietly: "'If I take the
wings of the morning, and dwell in the uttermost parts of the sea;" "Even there shall thy hand lead me, and thy right hand
shall hold me.'" Big Sister, not asleep: "Psalm 139." "Go to sleep, darling." "We're in the uttermost parts." "I know. So
is His hand." The card "Twelve days later" / "Osaka". On the act's map the three portraits go along the coast by the sea
path, through Osaka (now on the map), to the hills, the ship's timbers creaking (`g.journey`). Then, over the dark, Osaka:
"Everyone has a ladle. Everyone's going east. We're going the other way." "That man in the belt has looked at us twice.
Hats down, girls. We walk." Gonroku: "The magistrates have been thick in Osaka since the Kirishitan business." "Go north,
into the hills, till it's quiet." "North. Thank you, captain. You've carried us further than you meant to." "Twelve days of
fair wind. Never had twelve in a row. ...Don't tell the Funadama." And the cedar path in the hills (`edo-cedars`, at its
`enter`; no era card): the second leg. `edo.sailed`; the box of sushi gone; the hats on. Skipped, the same.

### Ledger for this leg

**Things that are carried**

| Thing | Comes from | Who can hold it | Used for |
| --- | --- | --- | --- |
| Box of sushi (`sushibox`) | Kihei's table (#23): O-Tami wraps the rest in a bamboo leaf and puts it in the hands of whoever is played | Whoever was fed it; then anyone it is handed to | Eaten on the ship, the whole box ("Best Tuesday ever.") |
| Silver coin | The Son's denarius, through Act Four (the hand-on gives it to Big Sister if nobody has it) | Big Sister | Shown to Sankichi: "Whose face is that?" Not yet: it goes through the door in Mom's fist at the act's end |
| Spare car key | Act Three | Mom | Shown to Sankichi: a cart that goes without a horse (five lines, and he stares) |
| Three pennies | The take-a-penny dish, Act Four | Little Sister (they come straight back) | #23: shown to Kihei: no hole. He gives them back. |
| One warm egg | Darlene, Act Four | Little Sister ("It's warm. It's MINE to keep warm.") | Shown to Kihei: "Keep your egg." Not yet: a constable on a path in the rain (#34) |
| Dad's pencil, the sticky note | Act Three | Whoever has them | Used on each other after #21: the sum written down (not needed) |
| Little Sister's pink flashlight | Act Three; given back to her at the hand-on | Little Sister | Not yet (#40) |

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| The Kirishitan board: silver for telling on anyone who prays to "the Kirishitan god" | #22, Sankichi reads it; "Then we pray quietly here." | The second leg: a hidden family under a storehouse, and a constable (#32 to #34) |
| "Nobody lies" | #22, the clerk: every answer true ("'From the east.' Mother. That was true.") | #34: the constable, and nobody lies |
| "Arigatō" | Sankichi, to Little Sister | The meal ("Husband. Your face."), the goodbyes ("Arigatō for the word."), and everyone after |
| "Okage-sama de": by your grace | #23, Kihei; Big Sister gives the act its name | The act's title, on its card |
| "Chickens KNOW." | Act Three, Act Four (Grandma Jolene's hens) | #24: every hen in Yui faces west |
| "I FIT." | Act Three, Act Four | #23: under the floor after the cat; and the storehouse's high window (#32) |
| The yellow boots | #22: "They're my BOOTS." | Kept the whole act, in every outfit; Sankichi wants to touch one (the LEFT one) |
| Psalm 139:9-10, "the uttermost parts of the sea" | The voyage, Mom at the stern rail; Big Sister gives the reference | "We're in the uttermost parts." "I know. So is His hand." |
| The baby asleep | #22 | Little Sister's grace (#23), and "Come back when the baby can talk." |

## Act Six, the first stretch: Suruga and the sea (#22's addition, #24 to #27, Casting Off, The Uttermost Parts)

<!-- SCENES-21A: new in round twenty-one, for MERGE-21's docs/PUZZLES-japan.md (in the manner of round twenty's first leg,
above it, whose #21 to #23 stand as built). It replaces round twenty's #24 card ("West"), its voyage ("The Uttermost
Parts") and the second half of its structure diagram; the leg's Yui part keeps everything else. -->
Round twenty-one makes the first leg a road and a ship. The hens still face west, and Mom's plan is now the obvious one:
the road, like everybody else. Dressed, the three walk out of Yui's west end along the Tōkaidō to Nishikurasawa, the rest
village at the foot of the Satta Pass, and up to the top, where a widow's pass blows onto a little stone figure's hat and,
given back, buys them the truth about Arai: not by road. Back in Yui, Kihei names the ship; Gonroku will not take women;
his wife, asked properly, changes his mind. At first light they cast off, and four days later they are on the deck off
Daiōzaki, with a compass to read and a boy's rice to save. The design is `briefs/out/edo2-design.md`, sections 3, 5 and 7;
the lines are WRITE-21A's (`js/content/lines/edo-c.en.js`; round twenty's in `edo-a.en.js`) and the talks are trees in
`js/content/talk/edo-c.js` (and round twenty's `talk/edo-a.js`, whose `kiheiTree` WRITE-21A edited); the act is
`js/content/acts/edo.js` (act 7, MERGE-21's beats); the scenes are `edo-village.js` and `edo-fishshop.js` (round twenty's,
changed, marked SCENES-21A), and the new `edo-kurasawa.js`, `edo-satta.js`, `edo-deck.js` and its close-up `edo-compass.js`,
with what this stretch shares in `edo-sea.js` beside them; the cut-scenes are `edo-castoff.js` (new) and `edo-sail.js`
(edited). Play it: `index.html?scene=edo-kurasawa&lead=mom&flags=edo.arrived,edo.clothes,edo.dressed,edo.hensWest`, or the
deck: `index.html?scene=edo-deck&lead=bigsis&flags=edo.arrived,edo.clothes,edo.dressed,edo.when,edo.west,edo.aboard`.

**The numbers.** In play order: #21 to #23 as built; **#24 West** (new: the hens, the road, the pass); **#25 A Captain Who
Says Yes** (round twenty's #24, its second half: Kihei names the ship, Gonroku, O-Masa); Casting Off; **#26 Etekō** and **#27
Don't Lift The Lid** (new, the deck); The Uttermost Parts. Names, beats and facts kept where they were.

### The three, together

Still the team of three, all on stage, played in turn (the party in every scene of the stretch). New for them here:

| | What only she can do here | What she will not do |
| --- | --- | --- |
| **Mom** | Ask O-Kuni good morning with no money, and be given a shell for the climb; give a pass back to the woman it describes; teach a twelve-year-old not to lift the lid; ask O-Masa properly, after the road | Use somebody else's pass ("No. It says fifty, with a mole by the right eye."); walk past the clerk before he has had his look; open what isn't hers to open ("We don't open what isn't ours to open.") |
| **Big Sister** | Read a ship's compass whose card runs backwards (#26: "That's backwards genius."), and call the heading in the sailors' word; write the Funadama's list in her note | Touch the stone figure, or take a thing off a holy figure's head; steer, or heave on a windlass ("I've read about what happens when you let go.") |
| **Little Sister** | Reach the Jizō's hat ("Sorry, sir. ...Got it."); ride in a palanquin she cannot pay for, for a moment; play charades with Kōta; give up a penny for the first time all act | Peek under the lid (she tries: "What did I just say?") |

**The clothes.** O-Tami's kimonos from #22 on (round twenty's), hats on outdoors; and now Big Sister's hair up, held with
O-Tami's own hairpin (`kanzashi`, an ear-pick at its end), from #22. On deck in the noon sun, the hats on.

**The sounds.** Yui's as built; at Nishikurasawa the shells hissing on the grill (the `sizzle` loop), gulls, the komusō's
few notes now and then; at the top the wind (`wind` loop), the gust as the paper flies, gulls below the road; on deck the
sea along the side (`sea` loop), the windlass, the sail filling, the timbers, the hiss of the boiling pot, a knock on the
mast step, and the Funadama's chirp (two small bright notes). The music: the act's `edo` on the road, `edo-sea` on deck and
in the close-up.

### Puzzle structure

```
                    #21, #22, #23 as built (#22 now ends with O-Tami's hairpin in Big Sister's hair)
                                              |
                       #24 West (Little Sister, then all; Yui, Nishikurasawa, the top of the Satta Pass)
                         the hens face west: "West it is, then. By the road, like everybody else."
                         dressed (#22): out of Yui's west end; O-Kuni's shell, "And your pass?", papers at Arai;
                         the top: the gust; the pass on the Jizō, lifted by Little Sister (or with Mosuke's pole);
                         used on the road (Mom will not); given back: Arai told kindly; the cloud lifts off Fuji;
                         the old shore; "Nobody's forgetting anybody."                         (edo.noRoad)
                                              |
                       #25 A Captain Who Says Yes (Mom; Yui)     [round twenty's #24, second half]
                         Kihei names the ship (after the road); Gonroku: no women aboard; O-Masa asked properly
                                              |   (+ #21's year: Big Sister will not sail out of a year she can't name)
                    Cut-scene: Casting Off (the goodbyes at first light; O-Masa at the boat; the windlass; the sail;
                               the first night, the box; "Four days later")                    (edo.aboard)
                                              |
                  +---------------------------+---------------------------+
          #26 Etekō (Big Sister)                              #27 Don't Lift The Lid (Little Sister, Mom, with Big Sister)
          the ship's clock (the close-up): the card runs      Kōta met (charades); the lid (Mom); the Funadama's
          backwards; English, the rooster, saru (the crew     list (Denzō, the first knock on the mast step); a
          freezes), the sea word, "Etekō."                    penny for a coin; she chirps
                  +---------------------------+---------------------------+
                    Cut-scene: The Uttermost Parts (the night, Psalm 139; "Eight days later" / "Osaka"; the
                               river mouth; the lighter; Gonroku's goodbye at the Dōjima steps)  (edo.sailed)
                                              |
                                  the Dōjima shore (Osaka: SCENES-21B's #28)
```

Goal of the stretch: **find the honest way west, get aboard, and earn a place on the ship.** The beats (`acts/edo.js`), each
with its fact: `edo.road` (#24, `edo.noRoad`; needs `edo.dressed`), `edo.west` (#25, `edo.west`; needs `edo.noRoad` and
`edo.fed`), `edo.castoff` (the cut-scene, `edo.aboard`; needs `edo.west` and `edo.when`), `edo.heading` (#26,
`edo.headingCalled`) and `edo.chirp` (#27, `edo.chirped`), both needing `edo.aboard`, in either order, and `edo.sail` (the
cut-scene, `edo.sailed`; needs both). The facts the staged hints read are the scenes': `edo.hensWest`, `edo.gust`,
`edo.passFound`, `edo.passBack` (#24); `edo.kiheiWest`, `edo.gonrokuNo`, `edo.gonrokuWife` (#25); `edo.compassRead`,
`edo.saruSaid`, `edo.seaWords` (#26); `edo.kotaMet`, `edo.lidDown`, `edo.funadamaList`, `edo.coinTraded` (#27).

### Location layout

Four new places: two paintings of the road (PAINT-21A), the deck and its close-up (PAINT-21B). Nishikurasawa and the top
are part of Yui on the act's map (leg 1: the map's Yui place holds all four scenes of the leg); the deck and the compass
are a place that is a point of the sea way ("At sea"), where every place refuses ("Yui. We're at sea. The map can wait.").

```
YUI (edo-village), as built, and now: the WEST END of the street (past the well, behind Kihei's house: the Tōkaidō on
toward the pass); the relay COURIER running through now and then, both ways; the KOMUSŌ walking west now and then.

NISHIKURASAWA (edo-kurasawa): the rest village at the foot of the Satta Pass, morning; one floor (the road and the rest place)
+-----------------------------------------------------------------------------------------------------+
|                FUJI across the bay, under its CAP OF CLOUD          the HACKBERRY on the 40th DISTANCE   |
| O-KUNI'S TEAHOUSE (thatch; the matted room; the bay       BAY, BOATS     MOUND; MOUNT SATTA, the CLIFF   |
| through its back): the BENCH, the NOREN, the GRILL of     YUI'S SHORE    ROAD cut across it              |
| turban SHELLS (SMOKE), the SIGNBOARD; O-KUNI behind      the PALANQUIN set down; SAKUJI and TORA squatting |
| her grill            SŌSHICHI by his TRUNKS                                   the KOMUSŌ, playing          |
| from YUI (left edge)   the ROAD (the Tōkaidō): the COURIER runs through          up the CLIFF ROAD (right) |
+-----------------------------------------------------------------------------------------------------+

THE TOP OF THE SATTA PASS (edo-satta): the cliff road, morning, wind; one floor (the road; the bank is not walked)
+-----------------------------------------------------------------------------------------------------+
|                 FUJI, enormous (its CAP OF CLOUD on, then lifted)              the bent PINE, leaning     |
|  the OLD SHORE under the cliffs (white water)    the BAY far below; IZU east;    toward Fuji; OKITSU's    |
|                                                  GULLS hanging in the wind       roofs, a TEMPLE roof     |
|  O-SHIGE on her stone, KYŪZŌ with her box   the JIZŌ (red bib, straw HAT; the PASS caught on it)        |
|  from below (left edge)   the ROAD, the EDGE (a bank of grass)   MOSUKE resting with his load            |
|                                                                         on west, to Okitsu (refuses) |
+-----------------------------------------------------------------------------------------------------+

ON DECK (edo-deck): Gonroku's coaster, the fifth day out, off Daiōzaki, noon; one floor (the near walkway, bow to stern)
+-----------------------------------------------------------------------------------------------------+
|  the great SAIL on its YARD (breathing)                    GULLS                                     |
|  DAIŌZAKI (the CAPE), the SEA in rows running past; SPRAY at the BOW; a floating CASK now and then     |
|  the ship's BOAT on the mats; the HOLD (BALES, CASKS)   the MAST in its iron RINGS   the WINDLASS (two   |
|  KŌTA at his HEARTH box and its rice POT   the MAST STEP (the Funadama)   sailors)   the DECKHOUSE      |
|  the BOW          DENZŌ by the mast        SEIJIRŌ on a bale       KANBEI by the COMPASS BOX; GONROKU    |
|                                                                    at the TILLER; the RUDDER's head      |
+-----------------------------------------------------------------------------------------------------+

THE SHIP'S CLOCK (edo-compass): a close-up, the compass box from above (nobody drawn; Step back to the deck)
   the BOX, its LID propped; the CARD: twelve marks cut anticlockwise (the RAT at the BOW MARK, the BOAR, the DOG, the
   ROOSTER at the right, the MONKEY, the SHEEP, the HORSE at the bottom, the SNAKE, the DRAGON, the HARE at the left, the
   TIGER, the OX), each with Kōta's ink animal; the NEEDLE trembling, its tip on the monkey; KANBEI's THUMB at the edge.
```

Ways: Yui's west end (or a use of its road or pass, once the way is open) to Nishikurasawa (`yui`); Nishikurasawa's left
edge back to Yui (`fromWest`, by the well), its right edge (or the cliff road, or the road) up to the top (`below`); the
top's left edge down to Nishikurasawa (`climb`), its right edge west to Okitsu, which refuses. The deck has no ways out; the
compass box opens the close-up, and Step back returns everyone where they stood.

### Cut-scenes and puzzles

```
#22's addition: O-Tami's hairpin        (in #22's step 4, the kimonos)
```
Between "It ends at my knees." / "Travellers hitch them up anyway. You're ahead of everybody." and "Pink for the small one",
O-Tami: "And not with your hair down. Not on a road. Sit." Big Sister sits on the step facing us; O-Tami stands behind her
and puts it up: "There. Up, and held with my own pin." Big Sister: "It's an ear-pick." O-Tami: "Of course it is. My
grandmother said a pin that's only pretty is a sin," "so they put a pick on the end, and now it's a tool." "...That isn't a
hairpin. That's a loophole." "Keep it. My grandmother would like it on a girl who reads." (`kanzashi` into Big Sister's
pockets, whoever is played) "Thank you. I'll use the pretty end." The pin is one of the three things #37 needs. (The
grandmother's story is a story: "one theory", as the design has it.) SCENES-21A: her hair is drawn up with the kimono itself
(PEOPLE-21B's `BIGSIS_HAIR_UP`), so she faces us on the step while the pin goes in, where the knot does not show.

```
Puzzle #24: West        (Act Six · Leads: Little Sister, then all · Yui, Nishikurasawa, the top of the Satta Pass)
Needs:        #22 (edo.dressed)
Setup:        The door they came through is gone. Little Sister at the hen yard (as built): "They're all looking the same
              way. Every single one. That way." "Chickens KNOW." "West is a very large direction." Mom, now: "West it is,
              then. By the road, like everybody else." (and, before the kimonos, "Once we look like everybody else. Not
              before."). (edo.hensWest)
Step 1:       Yui's west end, past the well: "The road out of the village, west, toward the pass. Everyone walks it but us."
              Not in their own clothes ("Not in these clothes, darling. We'd be a parade by the first mile."); not before
              the clerk, once in O-Tami's ("O-Tami sent us to the clerk first, darling. Let him have his look at us."); not
              before the hens ("We're not walking anywhere until we know which way, darling."). Dressed and written down:
              "West, girls. Hats down, and a good morning for everyone we pass." Nishikurasawa: "I smell something.
              Something on fire. Something GOOD on fire." "A teahouse at the foot of the pass. Everyone stops here before
              the climb." "And we've nothing to pay for any of it. Smile, girls. Don't stare at the grill."
              O-Kuni, at her grill: "Turban shells! Grilled in their own pots, hot from the sea and the fire." "Three of
              you, and not a coin between you. I can tell by the walk." Mom's good morning ("Good morning's free. The
              shells aren't. ...Wait there."), or Little Sister's ("Small people eat MORE."), brings one shell on a leaf, to
              share: "Here. One. Share it, and don't tell the road. For the climb." ... "I want the CURLY end." "Of course
              you do." "Arigatō, shell lady." (with Sankichi's word; else "Thank you, shell lady. Very MUCH.") "Polite, too.
              Have the curly end." (edo.shellShared). West: "Steep, short, and the best view on the road at the top. West,
              is it?" "And your pass, dear?" Big Sister: "We're IN a pass." "Not that kind. The paper kind. Your tegata."
              "Women going west need papers at Arai. Proper ones, with your face on them." "Thirty years I've watched
              women go up that road without them." "I've watched them come back down. Have a shell, I say. Then go home."
              "...Thank you for telling us. Truly." (edo.araiWarned)
              The bearers bargain before anyone asks ("Palanquin to the top! Cheap. Cheaper than walking, if you count your
              feet."); Little Sister: "How much is a ride?" "How much have you got?" "Three pennies." "...What's a penny?"
              "It's like your money, but with no HOLE." "Then it isn't money. It's a button with ideas." Tora: "We'd carry
              the little one for nothing." Sakuji: "We would NOT." She may sit in it ("Sitting's a fare too. ...Fine.
              Sit. Don't bounce." "It's COMFY. I'm bouncing a tiny bit. You can't tell."). Sōshichi, use first, pay later,
              gives Little Sister a print: "Here. For the child of the house. That's the custom." "We haven't got a house."
              "...Then for the child." (`toyamaprint`)
Step 2:       Up the cliff road. The top: "WIND. The wind wants my hat." "Hold your hats, girls. And hold the view. It's
              worth it." "The finest view on the Tōkaidō. Allegedly." Fuji is under its cap. Mosuke trudges past with his
              load and does not look. Up the road behind them, O-Shige and Kyūzō: "Kyūzō. Stop. I'm dying. I've died. Put
              the box down." "Yes, mistress." She sits on her stone. A gust: the folded paper flies out of Kyūzō's sash onto
              the Jizō's little hat, and nobody of theirs sees it go (Kyūzō least of all). "Something flew onto the stone
              man's HAT." "A paper, folded, wrapped in oiled paper. That's somebody's important something." (edo.gust)
Step 3:       The pass on the Jizō (the hat's whole area is the paper while it is there). Mom: "I'd have to reach over his
              head. Your sister's his height. It's her place." Big Sister: "I'm not taking things off a holy figure's head.
              Even things that aren't his." Little Sister, at the Jizō, exactly his height: "Sorry, sir. I'm just taking
              this. It isn't yours. ...Got it." Or Mosuke's load pole, asked of him ("Pole."): he holds it out to the hat,
              and the next to try uses it ("With his pole, then. Gently. ...There. Not a finger on him."). "It's a pass. A
              woman's. There's writing all over it, and it isn't ours." "Is it a TICKET? For the road?" (`shigepass`;
              edo.passFound)
Step 4:       Used on the road west, or on anyone: Mom will not. "No. It says fifty, with a mole by the right eye." "You
              can't read it." "I can read her face. It's hers." (after: "It's hers, girls. It goes back to her, and nowhere
              else.") Given back, by whoever has it (talking to her, or the pass used on her): "Excuse me. I think this is
              yours. It was on the little stone figure's hat." "That's my-- that's my PASS." "Kyūzō. Where was my pass?"
              "In my sash, mistress. Then in the wind." She gets up for it, goes white, then pink, and sits down again.
              "...Without that paper I'd never have got home. You could have kept it." "It isn't ours. It has your face in
              it, as far as I can tell." "'A woman of fifty, a mole by the right eye.' That's what the clerk wrote."
              (Big Sister, if Mom has said what she thought it said: "...Mom.") "I'm forty-nine. And it isn't a mole. It's a
              beauty mark. He had no poetry." (edo.passBack) "Sit. You gave it back. Nobody gives anything back on this road."
Step 5:       Asked about the road west, she tells them, gently: "West? Three women, with no papers?" "With none." "Then
              listen, because nobody else will tell you kindly." "At Arai there are two women. One reads your paper. The
              other reads you." "A woman leaving Suruga needs her paper from the town magistrate at Sunpu." "And if one went
              round? There must be another road." "Round the north of the lake there's another barrier. It looks at women
              too." "And a woman caught slipping round isn't killed. They give her away." "As a servant. To whoever asks."
              Mom: "...Then not by road." (edo.araiHeard) "There's no barrier on the water between here and Osaka. Find a
              captain." The cloud lifts off Fuji (a cross-fade of the painted cap: the same cloud is gone at Nishikurasawa
              too): "It came OUT." "...Oh, girls." "I take it back. Not allegedly." (edo.fujiClear) "And look down there.
              That was the road once. At low tide, between waves." "Forget your parent, forget your child, they called it.
              No one could look back." "So they cut this road high up the mountain. In 1655." (or Mosuke tells it first:
              "The old road. Down there. You went at low tide, between the waves.") Mom: "Nobody's forgetting anybody."
              (edo.noRoad: the beat.) Mosuke goes past the other way with a new load, and does not look.
Wrong tries:  The palanquin               -> "We can't pay, sweetheart, and they don't carry anyone for love." (and the
                                             bearers' "We would NOT.")
              The komusō, used (first)    -> Big Sister: "Nobody sees his face, and his kind may pass any barrier. I'm only
                                             saying." Mom: "That's a lie with a basket on it."
              The road on west, at the top -> before: Mom, "Not till I know what's at Arai." (or, before O-Kuni has said it,
                                             "Not yet. Everybody on this road carries a paper but us. I want to know why.");
                                             after: "Not by road. We said."
              The shells                  -> "A shell cooked in its own shell. That's efficient."
              The mound                   -> Sōshichi, the first time: "Forty from Edo, that one. I count them. Somebody has to."
              Fuji under cloud            -> "Fuji, with a little cap of cloud. It's dressed for travelling too."
              O-Masa asked properly first  -> (back in Yui, dressed and fed) "Walk up that road first. He'll say you could
                                             have walked. Then ask me." (SCENES-21A's line: #25 waits for the road)
Gives:        edo.road (edo.noRoad). Back down: O-Kuni, "Back down. They all come back down. Sit. The smell's free." "You
              were right about Arai. We're going by sea." "By sea. Good. The sea doesn't read papers."; O-Shige, after her
              goodbye, goes on down east to Edo and her grandson, Kyūzō behind her with the box.
Notes:        The pass is the act's first exactly-true temptation: it describes somebody else. The yakko penalty is said
              once, gently, by a kind woman, and Mom's answer ends it. The view is the painter's own, from our own place on
              the road. Kihei, asked about west before the road, names the road only: "...Try the road. Everybody does."
              (edo.kiheiRoad). The courier and the komusō are in Yui's street now too (round twenty-one's section 10).
```

```
Puzzle #25: A Captain Who Says Yes        (Act Six · Lead: Mom · Yui)        [round twenty's #24, second half]
Needs:        #24 (edo.noRoad) and #23 (edo.fed)
Steps:        As built, from "Kihei names the ship", which now comes after the road: "We tried the road. It isn't open to
              us. Is there another way west?" "You tried the road." "Everybody tries the road. ...There's a ship." "My
              sister's husband's ship is in the bay. Osaka, morning tide. Dried bonito." "He won't take you. ...Ask anyway.
              Ask the right one." (edo.kiheiWest) Then Gonroku's no (every argument fails, in weather) and his wife (as
              built, round twenty's #24 steps 3 and 4): O-Masa asked properly, dressed, fed, past the clerk and after the
              road; "...They sit in the stern, and they don't whistle." (edo.west)
Gives:        edo.west. The goodbyes and Casting Off follow, with the year worked out (#21: "Not yet. I won't sail out of a
              year I can't name. The year first, then the sea.").
```

```
Cut-Scene: Casting Off        (new; the beat edo.castoff: edo.aboard)
```
Played by the village after the goodbyes (round twenty's, unchanged, in the street before the shop at first light). The
card "Casting Off". On the beach by the tender, O-Masa: "My nephew cooks on that ship. Kōta. Twelve. Be kind about the
rice." "We will. Thank you, O-Masa. For the question as much as the answer." "You asked it properly. Go on, before he
changes his weather." The ship's boat rows them out (a picture over the stage, as the night at sea is: two sailors at the
oars, the three in its stern, Little Sister waving, Gonroku's ship at anchor ahead, Fuji pink at first light): "A boat to
get to the BOAT." "The ship's own boat. Big ships carry a little one. Like a pocket." "Wave to Yui, girls. Properly.
Somebody's watching." Aboard (a picture: the deck at anchor, the yard on the deck with the sail furled on it, two sailors at
the windlass): "Heave." "And heave." (the yard going up the mast a heave at a time, four heaves) Denzō: "Up she goes! Mind
your heads. Mind your HATS." The great sail falls open and fills: "It's BREATHING." "Woven, not sewn. A captain from Harima
thought of it." "I've never seen anybody proud of cloth before." "You've never seen THIS cloth." Seijirō counts them:
"Three. ...Cargo." "Passengers, I think." "Passengers pay. ...Cargo." Gonroku: "Stern. No whistling. Wind's fair. ...For
now." The first night (round twenty's ship by night, the girls on the coil of rope, the box between them): "We ate the WHOLE
box. On a boat. At night. Best Tuesday ever." "It isn't Tuesday. I have no idea what it is. ...It was a very good box." (the
`sushibox` gone from whoever had it). The card "Four days later"; the hats on; on the act's map the portraits go out along
the sea path from Yui to the ship's place at sea (`g.journey("edo", "yui", "sea")`, the timbers creaking); the deck, on the
mark `deck`. Skipped, the same: edo.aboard, the box gone, the hats on, the deck.

```
Puzzle #26: Etekō        (Act Six · Lead: Big Sister · the deck, the ship's clock)
Needs:        Casting Off (edo.aboard)
Setup:        The deck, the first time: "Day five at sea. I've counted every one of them. In fours, mostly." "I LIVE on a
              boat now. I'm a boat person." "Five days, and nobody has been ill over the side. I'm very proud of us." The
              ship's talk: "Daiōzaki. Past it, the Kumano-nada. Wind holds till dark. Maybe." "She hasn't chirped. Not once
              since the women came aboard. Five days." "...Can't see the card. ...Sun's on it." "Rice is burnt again." "And
              raw. Both at once. It's a gift, that boy."
Step 1:       Kanbei: "Girl. ...You read?" "Everything. Except Japanese." "...This isn't Japanese. It's animals." "Show me the
              card. I'll read it out to you." The compass box (or Kanbei) opens the close-up: the box's lid propped (it shows
              on the deck as open), the card, the marks, Kōta's little animals. Big Sister's first look at the needle: "The
              needle points north. So north is... the monkey?" Kanbei (beside the box): "The ship's clock tells you where the
              ship goes, girl." "That's all a ship wants to know." "The rat's fixed at the bow. And the marks run the wrong
              way round. On purpose." "...Go on." "So the needle sits on wherever we're going. That's genius." "That's
              backwards genius." (edo.compassRead) Step back: the deck, everyone where they stood.
Step 2:       The call (Kanbei, Big Sister's): "...Well? Call it, girl. ...The helm's waiting." English: "Monkey!" "...Monk-ee?"
              "Monk-ee." Gonroku: "Say it so the helm can hear it." The rooster: "West. The rooster. Isn't it?" "...Is the
              needle on the rooster?" "No. One along. We're not going west. We're going west-and-a-bit." "A ship is always
              going west-and-a-bit." Saru (once Little Sister has had it from Kōta): "Saru. ...My sister says that's the
              word for it." The crew freezes, Denzō's hand on the mast: "NOT that word." "Not at sea. It means 'go away', and
              the lady hears it." "...Wind's still with us. Nobody says it twice." "I'm so sorry. I didn't know. I won't say
              it again." "...You didn't know. She knows you didn't know. Probably." (edo.saruSaid)
Step 3:       The sea word: Denzō, asked ("...Etekō. At sea, it's etekō. Never the other one." "And a snake's the long thing.
              And a whale is Ebisu. Remember that one." "A word for everything you mustn't say. That's very well
              organized."), or Kōta, asked by Little Sister ("...Come here." "Etekō. Say it QUIET."). (edo.seaWords)
Step 4:       "Etekō." Kanbei: "Etekō." Gonroku: "Etekō. Hold her." "...The girl reads the clock." "I read a compass.
              Backwards. In animals. I'd like that on a plaque." (edo.headingCalled)
Wrong tries:  Reading it as a map (the first look, above); the rooster; the monkey's mark, used ("That's our heading. Now I
              have to say it so the helm can hear it."); any mark, used ("Touching the marks steers nothing. Calling the
              heading does."); the cape ("Daiōzaki, where one sea ends and the next begins."); the windlass ("I'm not strong
              enough, and I've read about what happens when you let go.")
Gives:        edo.heading.
Notes:        The reversed card and the sea words are real; calling a heading by the sea word for monkey is the game's joke.
              The needle trembles on its pin (the painter's three states, stepped by the close-up itself; still for less
              motion). Kōta drew the animals.
```

```
Puzzle #27: Don't Lift The Lid        (Act Six · Leads: Little Sister and Mom, with Big Sister · the deck)
Needs:        Casting Off (edo.aboard)
Setup:        Kōta at his hearth box, lifting the lid now and then (the painted pot, its lid propped beside it, then boiling
              again): "Ma'am. ...The rice isn't ready. It's never ready. Then it's burnt."
Step 1:       Kōta (Little Sister): "You're the small one. The one in the YELLOW boots." "I'm SEVEN. How old are you?"
              "Twelve. I'm the cook. Don't tell anybody about the rice." (edo.kotaMet) Charades: the Grump ("...The
              master!" "He's the GRUMP. That's his name now." "...Grump." "PERFECT."), the cat ("A yokoza!" "A WHAT?" "A cat.
              At sea you say yokoza."), the monkey ("Sa-- saru!" "Don't! Not at SEA. She hears." "...Sorry. I'm putting my
              arms DOWN."); his mother in Yui, her brother ("He's ten. He's somewhere else. We're finding him." "...At sea?"
              "Further.").
Step 2:       The lid (Mom): "You keep looking." "My mother always did the rice. I don't know when it's done." "Don't lift
              the lid. Listen to it." "When it crackles and smells like toast, off the fire. Then leave it alone." The pot
              boils; Little Sister, who has listened to every word: "I'll just PEEK--" "What did I just say?" "Can I look?"
              "No." "Can I look NOW?" "Listen." "...It's crackling." "And?" "It smells like TOAST." "Off the fire. Now leave
              it be." The crew eat: "...It's rice." "It's RICE rice." Gonroku: "Hm." Denzō: "That's praise. That's all the
              praise he's got, and he gave it." (edo.lidDown; the pot's lid on, left alone)
Step 3:       The mast step, knocked on by anyone (or Denzō asked): "What the shipwright sealed in, for her, the day she was
              built." "A pair of dolls. Two dice. Twelve coins, one mon each." "A woman's hair. The five grains. Rouge and
              powder. A comb and a pin." "I'm writing it down. I write everything down. Dolls, dice, twelve coins..." "She's
              got MAKEUP in there." "She's a lady." (edo.funadamaList: Big Sister's note shows the list from then on)
Step 4:       A penny for a coin (Little Sister shows Kōta her pennies): "A coin with no hole! How do you carry it?" "You
              don't. You lose it." "...Could I have one? For my mother. From across the sea." (a long look at them) "...Okay.
              ONE. Pick the shiny one." "Then you have this. My coin. The first coin I ever got at sea." "...She's never
              let one go before." "She gave away a penny. I'm writing that down." (three pennies become two: `twopennies`;
              the one-mon coin: `mon`; edo.coinTraded)
Step 5:       She chirps, after the last of the four: Kōta laughs (at the man's face on the penny, at the rice coming right,
              or at the lady's makeup) and from the foot of the mast come two small bright notes. "THERE. Did you hear her?"
              "She chirped. She's in high spirits!" Gonroku: "...She likes the boy laughing." "She LIKES us." Seijirō:
              "Three. ...Crew." (edo.chirped)
Wrong tries:  The mast step, after the list ->  "We don't open what isn't ours to open." "Also, it's nailed." (and after
                                                that, Denzō says the list again)
              The floating cask (now and then) -> Denzō: "Leave it! That's for Konpira, the sailors' god. Whoever finds it
                                                takes it on." "A message in a bottle. For a GOD." "Then it's the next ship's
                                                errand, darling. We have ours."
              Lifting the lid herself        -> "I'll just PEEK--" "What did I just say?" (in the waiting)
              The windlass                   -> (Big Sister) "I'm not strong enough..."
Gives:        edo.chirp.
Notes:        The Funadama's things, her chirp and the sea words are documented; Kōta's rice and the hearth box are the
              game's. The list is #37's clue: Big Sister's note, looked at, reads it ("The lady's things, in Dad's pencil: two
              dolls, two dice, twelve one-mon coins," / "a woman's hair, the five grains, rouge, powder, a comb and a pin.").
```

```
Cut-Scene: The Uttermost Parts        (as built, edited; the beat edo.sail: edo.sailed)
```
Played on the deck the moment #26 and #27 are both done. The card "The Uttermost Parts". Round twenty's night (the box is
gone, eaten on the first night): the girls asleep on the coil of rope, Mom at the stern rail, Psalm 139:9-10 ("'If I take
the wings of the morning, and dwell in the uttermost parts of the sea;" / "Even there shall thy hand lead me, and thy right
hand shall hold me.'"), Big Sister: "Psalm 139." "Go to sleep, darling." "We're in the uttermost parts." "I know. So is His
hand." The card "Eight days later" / "Osaka" (WRITE-21A's: the deck was the fifth day of twelve). On the map the portraits
go from the ship's place at sea along the sea path to Osaka. The river mouth (a picture: masts crowding the two rivers, the
city, a castle on the skyline with walls and turrets and no top): "Masts. Hundreds of them, standing in the river mouths
like reeds." "It's a city made of BOATS." "Their castle hasn't got a top." Gonroku: "Burned before my grandfather. They
never put it back." The lighter alongside: "Ship stays here. Everything else goes up the river by lighter. So do you." Kōta,
waving from the rail: "Mother gets the penny first thing. I'll tell her it crossed the sea." "Tell her it's from the girl in
the yellow boots." Denzō: "Mind the river. Mind EVERYTHING!" Up the river to the Dōjima steps (a picture): Gonroku, in the
lighter at their foot: "The magistrates have been thick in Osaka since the Kirishitan business." "Go north, into the hills,
till it's quiet." "North. Thank you, captain. You've carried us further than you meant to." "And don't tell anybody anything
true." "That's the only kind I've got." (he nearly smiles) "Twelve days of fair wind. Never had twelve in a row. ...Don't
tell the Funadama." as the lighter goes. The Dōjima shore, on the mark `landing` (SCENES-21B's; its first words are its
own). Skipped, the same: edo.sailed, the hats on, the landing.

#### The hints, stage by stage

| Beat | Stage (the fact that ends it) | Mom | Big Sister | Little Sister |
| --- | --- | --- | --- | --- |
| #24 `edo.road` | the hens not seen (`edo.hensWest`) | `hint.edo.road.mom` | `.bigsis` | `.lilsis` |
| | not yet at the top (`edo.gust`) | `.mom.2` | `.bigsis.2` | `.lilsis.2` |
| | the pass on the Jizō (`edo.passFound`) | `.mom.3` | `.bigsis.3` | `.lilsis.3` |
| | the pass not given back (`edo.passBack`) | `.mom.4` | `.bigsis.4` | `.lilsis.4` |
| | O-Shige not heard (`edo.noRoad`) | `.mom.5` | `.bigsis.5` | `.lilsis.5` |
| #25 `edo.west` | Kihei not asked after the road (`edo.kiheiWest`) | `hint.edo.west.ship.mom` | `.ship.bigsis` | `.ship.lilsis` |
| | the ship named, Gonroku not asked (`edo.gonrokuNo`) | `.ship.mom.2` | `.ship.bigsis.2` | `.ship.lilsis.2` |
| | then round twenty's | `hint.edo.west.mom.2` | `hint.edo.west.bigsis`, `.bigsis.2` | `hint.edo.west.lilsis.3` |
| Casting Off | (one) | `hint.edo.castoff.mom` | `.bigsis` | `.lilsis` |
| #26 `edo.heading` | the clock not read (`edo.compassRead`) | `hint.edo.heading.mom` | `.bigsis` | `.lilsis` |
| | read, nothing wrong yet | `.mom.2` | `.bigsis.2` | `.lilsis.2` |
| | saru said (`edo.saruSaid`), no sea word | `.mom.3` | `.bigsis.3` | `.lilsis.3` |
| | the sea word known (`edo.seaWords`), not called | `.mom.4` | `.bigsis.4` | `.lilsis.4` |
| #27 `edo.chirp` | Kōta not met (`edo.kotaMet`) | `hint.edo.chirp.mom` | `.bigsis` | `.lilsis` |
| | the lid not right (`edo.lidDown`) | `.mom.2` | `.bigsis.2` | `.lilsis.2` |
| | the list not heard (`edo.funadamaList`) | `.mom.3` | `.bigsis.3` | `.lilsis.3` |
| | the coin not traded (`edo.coinTraded`) | `.mom.4` | `.bigsis.4` | `.lilsis.4` |

### Ledger rows for this stretch

**Things that are carried**

| Thing | Comes from | Who can hold it | Used for |
| --- | --- | --- | --- |
| O-Tami's hairpin (`kanzashi`) | #22: O-Tami puts Big Sister's hair up with it, and lets her keep it | Big Sister | #37: the rabbit's ear (Little Sister's fingers); back in Big Sister's hair after |
| Peddler's print (`toyamaprint`) | #24: Sōshichi, "for the child of the house" | Little Sister | A keepsake (shown to Senzō in Osaka: "That's one of ours, copied badly in Toyama.") |
| O-Shige's pass (`shigepass`) | #24: lifted off the Jizō's hat | Whoever lifted it | Given back to O-Shige (the wrong try: used on the road west, or on anyone) |
| Three pennies, then two (`twopennies`) | Act Four's take-a-penny dish | Little Sister | #24: "Three pennies." "...What's a penny?"; #27: one to Kōta for his mother; #35: one to O-Fusa |
| One-mon coin (`mon`) | #27: Kōta's, "the first coin I ever got at sea" | Little Sister | #37: the square post under the rabbit's waves (Mom's wrist); then to O-Ume "for your rice balls" |
| Dad's sticky note, with the list | #27: Big Sister writes the Funadama's things in it | Big Sister | #37: what a ship gives its lady (a comb, a pin, twelve one-mon coins) |
| Box of sushi (`sushibox`) | #23 (as built) | whoever was fed it | Eaten on the first night (Casting Off) |

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| "And your pass?" "We're IN a pass." | #24, O-Kuni | The pass on the Jizō; "Then not by road." |
| A woman's pass that describes somebody else | #24, the Jizō's hat | Given back: the truth about Arai, and the honest way west (a ship) |
| "Forget your parent, forget your child" | #24, the old shore | "Nobody's forgetting anybody." (Mom) |
| Fuji under its cap of cloud | Yui, Nishikurasawa, the top | "It came OUT." (and gone at Nishikurasawa ever after) |
| O-Masa's nephew, Kōta, twelve | Casting Off: "Be kind about the rice." | #27: the lid; the penny for the coin; the chirp |
| The Funadama hasn't chirped since the women came aboard | The deck's first words (Denzō) | #27: she chirps when the boy laughs; and #37's lock chirps the same |
| What a ship gives its lady: a comb, a pin, twelve one-mon coins | #27, Denzō's list, in Big Sister's note | #37: the pin, the coin and the comb open the women's hall |
| "Etekō" | #26/#27: Kōta's whisper, or Denzō | The heading called; "I'd like that on a plaque." |
| Little Sister gives up a penny for the first time | #27 | #35 (a penny for luck to O-Fusa); #38 (the Son has one) |
| Gonroku: "And don't tell anybody anything true." | The Dōjima steps | "That's the only kind I've got." (the act's rule) |

## Act Six, the second leg: Osaka (#28 to #31, and "The Kyoto Boat")

<!-- SCENES-21B: new in round twenty-one. MERGE-21 joins this with SCENES-21A's and SCENES-21C's parts into docs/PUZZLES-japan.md. -->
Twelve days from Yui, the last week of April 1830, the pilgrimage to Ise in flood: Osaka, by the river. The lighter that
brought them up from the ship at the river mouth leaves the three of them at the top of the stone steps on the Dōjima
shore, where the rice dealers live; from there a merchant street with a print shop and a crossroads, and in the grounds of
Naniwa Shrine the Inari puppet theatre, backstage. They are hungry, they have no ladle and no money, and the magistrate's men
are walking the shore looking at faces; they will not pretend to be what they are not, and they must not be asked questions
(Mom would answer them). The leg begins on the Dōjima shore, on its mark `landing`, as the Uttermost Parts leaves it
(SCENES-21A's `edo-sail`), and ends when "The Kyoto Boat" hands on to the cedar path in the hills (`edo-cedars`, on `enter`).
The design is `briefs/out/edo2-design.md`, sections 2, 5 and 7; the lines are WRITE-21A's (`js/content/lines/edo-c.en.js`;
`ids.md` says when each is said) and the talks trees in `js/content/talk/edo-c.js`; the beats are in `js/content/acts/edo.js`;
the three scenes are `js/content/scenes/edo-dojima.js`, `edo-street.js` and `edo-theatre.js`, with what they share in
`edo-osaka.js` beside them; the cut-scene is `js/content/cutscenes/edo-boat.js`. Play it: `index.html?scene=edo-dojima&lead=mom`,
then the leg's start as LEG_START.osaka has it (the travel clothes on; Big Sister's hairpin; Little Sister's two pennies, the
one-mon coin and the peddler's print): `tests/briefs-out/play-edo-osaka.py` sets it up by script.

### The three of them, in Osaka

They go together, a party of three, through all three places. Outdoors (the shore, the street) the travel hats are on
(PEOPLE-20's outfit `edo`); in the theatre they hang on their backs (`edo-hatback`), and from Jūbei's "Robes. Now." until the
boy has knelt at his mother's door the girls are in the puppeteers' black (PEOPLE-21B's `edo-kurogo`: hood and robe, Little
Sister's yellow boots showing under it). While they are in black, their looks at each other are the theatre's own ("My
youngest, in a black hood. You can still see the boots. You always can."). Nobody walks during the show: the girls do their
parts from the rail, Mom watches from her seat (the scene's `still`).

**The people of Osaka** are PEOPLE-21A's: O-Natsu, the rice dealer's wife, at her alms stall, and later at the crossroads;
the pilgrims in her line (an Awa father, an Awa mother with a baby on her back, an old pilgrim from Kii, a boy with a ladle
bigger than his face); Kyūhachi, who has been through the line four times; Rihei among the dealers, wet; Kurata the dōshin
and Tatsu his thief-taker, walking the shore; in the street Senzō at his printing bench, the komusō playing at a door, the
yomiuri pair chanting down the cross street; in the theatre Jūbei, the chanter and the shamisen player on their dais, and
Tatsu in the front row. Kurata and Tatsu are never answered by the family: on the shore the one who answers is O-Natsu, who
has made it true ("My helpers.").

**What moves.** On the shore the rice pot and the kettle steam, the hearth's coals glow, the noren stirs, lighters pass on
the river both ways (PAINT-21C's painted frames), the river glitters, and now and then a water man's bucket splashes the
dealers (PAINT-21C's five frames, with its sound) and the price runner sprints off along the road (PAINT-21C's run frames,
moved by the scene). In the street the prints and the shops' noren stir, two birds wheel over the roofs, and the komusō
plays his few notes now and then. In the theatre the lamp's flame flickers, motes turn in the house's shafts of day, and in
the show the roof hatch's day falls on the stage (PAINT-21D's light pictures). Music: `edo-city` on the shore and in the
street (with a crowd's murmur under it), `edo-theatre` in the theatre.

### Puzzle structure

```
                 (SCENES-21A's "The Uttermost Parts": the night at sea; Osaka; the river mouth; the lighter; Gonroku's goodbye)
                                        |
                 the landing: up the river steps; "Everybody here has a ladle but us."          edo.landed
                                        |
                 #28 The Dōjima Shore (all three, Mom first; the shore)
                     no ladle: "We could BORROW a ladle." "And then we'd be lying with a spoon."
                     Mom asks to help: O-Natsu's paddle (the kitchen is hers)                    edo.paddle
                     the pot (Mom)  |  the rice balls, bale-shaped (Big Sister)  |  the pickle, one slice each (Little Sister),
                                    |                                           |  and the man who comes round again: his fifth
                     the line fed; Kurata along it: "Who are these three?" "My helpers."         edo.vouched
                     their supper on the river steps; the paddle back; "Come with me."
                                        |
          +-----------------------------+------------------------------+
          |                                                            |
   #29 What The Road God Said (Mom; the crossroads)            #30 Berlin Blue (Big Sister; the print shop)
       the boxwood comb; Mom's own prayer (Jeremiah 31:17)         Senzō prints by eye: a blurry famous man (to Little
       the first words: "...a boy, alive and well, calling         Sister); the marks; the laying, in order: corner, side,
       for his mother!"; the chant: a boy's voice at Shosha        rub: a clean print in the new blue        edo.registered
       the men; the pair run; the sheet caught; Tatsu follows      the sheet (from #29), read aloud: the lock no comb
       the comb and the slip, given to Mom      edo.combGiven      or pin opens                              edo.sheetRead
          |                                                            |
   #31 Three To A Puppet (the girls; Mom in the audience; the Inari theatre)              (either order: #30 before or after)
       somewhere dark, somewhere crowded: in at the back door; Jūbei; "In black, you're not there."
       the robes; the rehearsal; Mom out front beside Tatsu; the show: three cues; the house weeps
       Jūbei asks who they are: the truth; the road round Osaka                                  edo.troupeTaken
          +-----------------------------+------------------------------+
                                        |
                 Cut-scene: The Kyoto Boat (Hachikenya; the haulers; the food boats; the ferry; the rain)   edo.boated
                                        |
                 (the third leg: round twenty's #32 Under The Cedars)
```

The beats (`js/content/acts/edo.js`), each with its fact: `edo.alms` (#28, the family, needs `edo.sailed`: `edo.vouched`),
`edo.heard` (#29, Mom: `edo.combGiven`), `edo.read` (#30, Big Sister, needs `edo.vouched`: `edo.sheetRead`; its reading needs
the sheet #29 catches), `edo.troupe` (#31, the girls, needs `edo.combGiven`: `edo.troupeTaken`), and the cut-scene `edo.boat`
(needs `edo.troupeTaken` and `edo.sheetRead`: `edo.boated`). The scenes' facts the staged hints read are the act file's head
comment's: `edo.paddle`, `edo.fedPilgrims`; `edo.combAsked`, `edo.heardShosha`, `edo.sheetCaught`; `edo.marksSeen`,
`edo.registered`; `edo.backstage`, `edo.hooded`, `edo.rehearsed`, `edo.momSeated`, `edo.cue1`, `edo.cue2`, `edo.cue3`. The
scenes' own beside them: `edo.landed` (the landing played), `edo.potServed`, `edo.ballsShaped`, `edo.pickleServed`,
`edo.fifthCaught` (#28's tasks), `edo.supped`, `edo.streetSeen`; the trees' own: `edo.natsuMet`, `edo.followed`, `edo.senzoMet`,
`edo.jubeiMet`, `edo.ruleHeard`, `edo.rehearsedLeft`, `edo.rehearsedFeet`. While #29 and #30 are both open (and then #30 and
#31), each of the three gets the hint of the beat she leads, and the one who leads neither the first open one's (the
engine's rule): after the supper Mom's hint is the crossroads and Big Sister's the print shop.

### Location layout

Three places, one painting each, all in the Osaka place of the map of Japan (the second leg: the map refuses Yui behind them,
"Yui is twelve days back by sea. A penny's on its way there, with Kōta."). The shore and the street are joined at the
shore's right edge and the street's left; the street and the theatre at the street's right edge (the drum tower is its
sign) and the theatre's back door.

```
THE DŌJIMA SHORE (edo-dojima): Osaka, the rice dealers' quarter on the river, about four in the afternoon
+----------------------------------------------------------------------------------------------------+
| the SKY in haze; across the RIVER the domains' white WAREHOUSES; far up it, the CASTLE (no keep)      |
|  O-NATSU'S HOUSE (lattice, NOREN, bales)       LIGHTERS on the river         the high timber BRIDGE   |
|  her ALMS STALL: the SANDALS, the rice POT     the river STEPS (Here:        the RICE MARKET: the     |
|  on its hearth, the TUB of pickled radish,     the lighter left them at      DEALERS, hands up; the   |
|  the TRAY of rice balls, the KETTLE; O-NATSU   the top)                      WATER MEN and a BUCKET;  |
|  the pilgrims' LINE (four), KYŪHACHI                                         RIHEI; now and then the  |
|                                     KURATA and TATSU walking the shore      RUNNER  -> into the TOWN |
+----------------------------------------------------------------------------------------------------+

SHINSAIBASHI-SUJI (edo-street): Osaka, a merchant street at a crossroads, late afternoon
+----------------------------------------------------------------------------------------------------+
| ROOFS; the FIRE-WATCH TOWER over the cross street                     far off, the DRUM TOWER        |
|  SENZŌ'S PRINT SHOP, open: PRINTS on lines, TOY PRINTS;   the cross street: the YOMIURI pair (until   |
|  the BENCH: the BLOCK and its two marks, the PAD, the     they come round)    the KELP SHOP, the     |
|  pot of BLUE, the SHEET on its stand; SENZŌ behind it     MEDICINE signboard, the COMB sign, the     |
|  <- to the shore       the ROAD GOD at the CROSSROADS: O-NATSU      the KOMUSŌ    WATER-SELLER  -> to |
|                        (after #29: KURATA and TATSU at the corner)                    the theatre    |
+----------------------------------------------------------------------------------------------------+

THE INARI THEATRE (edo-theatre): backstage, looking across the stage to the house, afternoon
+----------------------------------------------------------------------------------------------------+
|  the RAFTERS; the high WINDOWS                                                                       |
|  the PUPPETS on their rail      the masking CURTAIN    the AUDIENCE on its mats; TATSU, front row    |
|  the BACK DOOR (<- the street)  the HEADS on a shelf     the SET: the village GATE, the HOUSE FRONT  |
|  the ROBES on their peg  the BOXES  the LAMP   the STAGE RAIL    the chanter's DAIS: the CHANTER, the |
|  the BOY PUPPET on his STAND; JŪBEI           the STAGE's boards  SHAMISEN player, the BOOK          |
|  (Mom goes round to the house through the gap at the wing wall's end: a floor of its own, by script)|
+----------------------------------------------------------------------------------------------------+
```

### Cut-scenes and puzzles, as built

```
The landing        (the end of SCENES-21A's "The Uttermost Parts"; the shore's own, once)
```
The lighter pulls away down the river from the foot of the steps, and the three come up them (faded in at the top: nobody
walks the flight); `edo.landed`. Big Sister: "Rice. Rice in bales, rice on boats, men shouting about rice." Mom: "And a line
of people with ladles. Everybody here has a ladle but us." Little Sister: "I'm HUNGRY. I'm hungry in a whole new city."
(Said by the shore the first time, unless the cut-scene before it has said them.)

```
Puzzle #28: The Dōjima Shore        (Act Six · Leads: all three, Mom first · Osaka, the Dōjima shore)
```
- **No ladle.** The stall, used before the paddle, by any of them: a kind look and a shake of the head (Little Sister: "I
  held out my hands. The lady smiled and shook her head. NICELY."); the first time, Little Sister's plan and Mom's answer:
  "We could BORROW a ladle." "And then we'd be lying with a spoon." Kyūhachi's offer (Mom asks how many times he has been
  fed): "I'll lend you my ladle. For a share. Fair's fair." "No, thank you." "Nobody ever says yes." Each of the stall's
  things before the paddle is not theirs to touch (Mom at the pot: "It isn't my kitchen, darling. Not unless I'm asked into
  it."). The way into the town refuses: "Not yet. We've had nothing since the ship, and nobody walks a city hungry."
- **The paddle.** Mom's question to O-Natsu: "May I help? I've run church suppers for two hundred. This can't be worse."
  "..." "A supper for two hundred. I believe you. Here." She hands Mom her rice paddle (`paddle`; Mom holds it out). Big
  Sister: "In Japan the paddle is the key." O-Natsu: "Pot's yours. Rice balls, the tall girl. Pickle, the little one, a slice
  each." (`edo.paddle`.) Now the way into the town says "Not without thanking her, darling."
- **Serving.** Behind the stall, a job each, by the right one of them (the wrong one: "That's somebody else's job. Mine is
  bales."): Mom at the pot ("One scoop in every ladle, and a smile. Next. ...Next.": `edo.potServed`); Big Sister at the tray,
  O-Natsu showing her ("Wet your hands. Salt. Now press it into a bale. A little bale." "Bale-shaped. The Osaka standard. I'm a
  standard.": the tray half full, `edo.ballsShaped`); Little Sister at the tub ("One pickle. One pickle. One pickle. ONE
  pickle. You get one.": `edo.pickleServed`), and at that Kyūhachi walks up from his place to the front of the line, his ladle
  out. Her next go at the tub catches him: "You had one. And one. And ONE. And one." "...That's four. This is five." "FIVE is
  too many." O-Natsu: "Give him the pickle. He'll be back tomorrow either way." (`edo.fifthCaught`; he goes back to his place.)
  All three done (in any order): O-Natsu: "That's the line. That's the whole line. ...Three of you, and I'm early."
  (`edo.fedPilgrims`), and the pilgrims go on east with a bow.
- **"My helpers."** Kurata comes along the shore to the stall, Tatsu at his back. "O-Natsu. ...Who are these three?" "My
  helpers." He takes a rice ball and looks at it. "...There'll be a notice about all this." On he goes; Tatsu stares at the
  three of them, and follows him. Big Sister: "'My helpers.' Every word of it true." Mom: "She made it true. She handed me the
  paddle." (`edo.vouched`: the beat.)
- **Their supper.** O-Natsu's tree goes straight on: "Sit. The last of the pot is the helpers'. That's my rule, and I've just
  made it." They sit on the coping at the top of the river steps; Little Sister's grace, in her own words ("Thank You for the
  rice, and the pickle, and for O-Natsu, and for her boy." "Bring him HOME. Amen."); a rice ball each; Mom: "Thank you. You fed
  us before we'd done a thing, and then you let us do it." "You did plenty. Eat." "When you've done, I'm going to the
  crossroads, to ask after my boy." "Come with me. It takes two mothers to stand still that long." "Of course I'll come." The
  paddle goes back, clean (`edo.supped`), and the way into the town is open.
- **Wrong tries**: the water men (Little Sister close enough to be splashed, the bucket's water over her: "They SPLASHED me.
  I wasn't even shouting."), the rice market (Big Sister: "The rice market. They're not buying rice. They're buying paper that
  says rice." Mom: "Don't explain it, darling. Not on an empty stomach."), the lighters ("Ours has gone, sweetheart. Osaka it
  is."), the castle with no top ("The castle's got no TOP. Somebody forgot the top."), the steps (the lighter has gone), the
  magistrate's men ("Not him, girls. If he asks me anything, I'll answer it. Truthfully."; Tatsu: "Let him stare, darling.
  Staring isn't asking."), Kyūhachi's ladle. The pilgrims each have two lines of their own (the Awa father: "Across from Awa
  by boat, and the rest on our feet. Thank you for asking."). Rihei, splashed every day: "Rihei. Rice. Wet. Every day of my
  life."
- Notes: the alms on the Dōjima shore are in an 1830 Osaka chronicle; the stall's things (rice balls, a slice of pickled
  radish, tea, straw sandals) are the 1830 lodges' and Osaka's 1771 ones; the water men's splash after the close and the
  runners with the price are documented. "My helpers." is the act's rule at work. The two-step pickle (the fifth time round
  caught on her second go) is the scene's staging of WRITE-21A's FIFTH; the supper on the steps' coping is the scene's.

```
Puzzle #29: What The Road God Said        (Act Six · Lead: Mom · Osaka, the merchant street)
```
Up from the shore the first time (`edo.streetSeen`): "SHOPS. A whole street of shops. And curtains. And a drum." "Kelp shops
and bookshops. This street is famous for both. I'm home." O-Natsu waits at the crossroads by the road god, her comb in her
hair. Down the cross street the yomiuri pair are chanting to the people there (a sheet tried for: "Four mon a sheet." Little
Sister: "I've got ONE mon. And it's not for papers. It's a souvenir."). The drum tower's way, before anyone is following them:
"A theater, darling, and we haven't a reason or a coin."
- **The comb.** O-Natsu: "Here. This corner. Don't laugh at me, any of you." (Mom: "Nobody's laughing. Tell me what to do,
  and I'll stand where you put me.") "You stand where the roads cross, holding a boxwood comb, and you ask." "The first words
  a stranger says as he passes are your answer." Big Sister: "Boxwood is tsuge. It sounds like 'to tell'." "Stand with me.
  Two mothers. The road god hears two better than one." Mom: "I'll stand with you. I won't ask your road god. I'll ask mine, if
  I may." "Ask whoever listens. I'll take any answer." Mom beside her, her head bowed, her hands folded: "'And there is hope
  in thine end, saith the LORD, that thy children shall come again to their own border.'" Big Sister: "Jeremiah 31:17."
  (`edo.combAsked`.)
- **The first words.** The pair come up the cross street to the corner, chanting: "...a boy, alive and well, calling for his
  mother!" O-Natsu: "That's my answer. He's well! He's well, and he's calling for me." Little Sister: "She's laughing and crying
  at the SAME time." Mom: "That's what it looks like, darling, when the news is good."
- **The chant**, line and line about: "Yomiuri! We read it, you buy it! A strange story from Harima!" "At the foot of Mount
  Shosha, by Himeji, there's a hall for women." "And every sunset, in that hall, a boy's voice speaks!" "In a tongue nobody on
  earth has ever heard!" "The monks have locked the door, and nobody living can open it!" "Four mon! Four mon, and you'll know
  it before your neighbour does." Mom: "A boy's voice. A language nobody knows." Big Sister: "English." Little Sister: "It's
  HIM." (`edo.heardShosha`.)
- **The men.** Kurata and Tatsu round the other corner. "Strange stories. On a corner. With a picture. ...Tatsu." "Run."
  "Running." (the pair off along the street); a sheet flutters down, and Big Sister has it: "Got it. ...I can't read a word of
  it." (`sheet`: `edo.sheetCaught`). Kurata: "There'll be a notice. There's always a notice." Tatsu: "...Three tall women. In
  hats." (`edo.followed`: from here he follows them; he and Kurata stand at the corner until they go to the theatre.)
- **The comb, given.** "Here. It told me. Let it tell you." Mom: "It's beautiful. I'll keep it. I'll do my asking the way I do
  it." "There's a temple at every turn of the road west. Leave a slip for my boy." "I will. I promise." (`comb`, `natsuslip`,
  Mom's: `edo.combGiven`, the beat.) After: "He's well. He's calling for me. I'll have the house swept before he's home."
- **Wrong tries**: buying a sheet (above), the road god (Big Sister: "I'm not touching him. I'm not even pointing at him. I'm
  pointing near him."; Little Sister: "I said good evening. He's busy minding the roads."), the medicine signboard (the first
  time anyone tries it: "U-ru-yu-su." "That doesn't sound like any word I know." "It's MEDICINE. Medicine never sounds like a
  word."), the theatre before Tatsu follows.
- Notes: the crossroads comb is in a book finished in 1830 (a women's custom); the pair chanting in turn, the price and the ban
  are documented; the answer coming from the chant is the game's. Mom's faith and O-Natsu's custom stand side by side.

```
Puzzle #30: Berlin Blue        (Act Six · Lead: Big Sister · Osaka, the merchant street, the print shop)
```
Senzō at his bench in the open front, alone (his paper boy is on the road to Ise), his blue landing a hair to the left.
Little Sister may show him Sōshichi's print: "Toyama! They copy Edo's actors, badly. Keep it. It's worth less than the paper."
"I LIKE it." "Then it's worth exactly what you think. That's printing." Before Big Sister has seen the marks, the bench's three
small places are only things on a bench ("His block. I'd only touch it with his paper in my hands and his yes.").
- **The marks.** Big Sister: "May I watch you print? Closely? I won't touch." "Watch! My paper boy's on the road to Ise, so
  watch closely and pity me." He prints one by eye, and the blue comes up a hair to the left: Little Sister, coming over to
  the bench: "That's a blurry famous man." "Every first one is." "For the small one. A famous man, with his blue ghost. Don't sell it." (the spoiled sheet
  to Little Sister: `blueprint`.) Big Sister: "There's a mark cut at the block's corner. And another along its edge." "The paper
  goes into the corner and against the edge, so every color lands true." "That's the idea. I've been doing it by eye. My eye
  lands a hair to the left." "May I lay the paper? I have very straight hands." "Lay away! Corner first. Then the side. Then I
  rub." (`edo.marksSeen`.)
- **The laying**: three small places on the bench (generous areas round PAINT-21C's small shapes), Big Sister's: the corner
  mark ("Corner into the corner mark."), the side mark ("Edge against the side mark."), then Senzō's pad ("And I rub. ...And
  lift."). In order: "Look at that. Look at THAT. Every line where it should be." "Berlin blue. It came last year. In Edo they're
  making whole pictures in it." "An actor at home, in a robe of the new blue. I registered it. That's the word." (the sheet on
  its stand clean: `edo.registered`). Out of order, its own line, and a ghost again ("A ghost again. Corner, side, then me. In
  that order. Again."): the side first ("Side first? No. Everything depends on the corner. Corner first."); the pad first ("Rub
  what? There's no paper on it yet.": he slaps one on by eye); the corner and then the pad, with no side. The laying starts
  again from the corner after any ghost (and after a game is loaded).
- **The sheet, read.** With the paper laid in order and the sheet caught, Big Sister (or Mom) asks him to read it: "Ha. Ha.
  ...I've never seen it before in my life. Nice blue, isn't it." "...Draw the curtain a little. Thank you." (He glances up the
  street and down, and holds it close.) "'At the foot of Mount Shosha, by Himeji, there is a hall for women.'" "'Every sunset a
  boy's voice speaks in it, in a tongue unknown to man or fox.'" "'The novice who kept its lamp ran out in fright and locked the
  door behind him.'" "'Nobody living can open that lock.'" "'Every woman in Harima has tried her comb and her pin in it.'" "'The
  abbot says it is not to be broken, and whoever opens it may go in.'" "And there's the lock in the picture: a rabbit running on
  waves. Lovely water." "A BUNNY lock." "A lock no comb or pin will open, and a boy's voice behind it." "Then that's where
  we're going." (`edo.sheetRead`: the beat; the sheet's look is the reading from now on.) Little Sister, after: "Why is there a
  hall just for LADIES?" "Women don't go up Mount Shosha. They stop at that hall, and leave their slips."
- **Wrong tries**: the actor prints ("All actors. Osaka does actors. Edo does pretty ladies. I read a book."), the toy prints
  (Little Sister wants all of them), the pot of blue ("The new blue. 1830 is the year the prints went blue. I'm IN it."), the
  peddler's print shown to him.
- Notes: actor prints as Osaka's trade, toy prints, Berlin blue new in 1829-30, registration marks and one block a colour are
  documented; a printer quietly printing the forbidden sheet is the game's. Staging decision: Senzō's demonstration print is
  the first ghost (WRITE-21A's LAY.ghost said there, where the design's "the first one always does" puts it), so the spoiled
  print reaches Little Sister in every game; every ghost after it is "again".

```
Puzzle #31: Three To A Puppet        (Act Six · Leads: Big Sister and Little Sister; Mom in the audience · the Inari theatre)
```
Tatsu is following three tall women; Mom: "Somewhere dark. Somewhere crowded. Follow the drum, girls." In at the back door
(`edo.backstage`): "It's DARK. And it smells like dust and glue." "Backstage. ...Oh. Oh, I like it here." Jūbei: "The last
piece of the day, and a boy with no left hand and no feet." "My left-hand man and my feet man both ran off to Ise yesterday."
"Everyone in Osaka has run off to Ise except the magistrates."
- **Black.** The robes on the peg (Big Sister asks who wears them): "The hands. They wear black, and hoods. The house agrees
  not to see them." Big Sister: "In black, you're not there. It's the rules." Mom: "It's not a lie if everybody knows." The
  girls offer ("We could be the hands. My sister and I. We're quick, and we can be quiet."; Little Sister: "I'm GOOD at feet.
  I've got two."); Jūbei looks at them, at the time, at the robes: "..." "The tall one, the left hand. The small one, the feet.
  Robes. Now." (both girls into `edo-kurogo`; the peg empty). Big Sister: "Three to a puppet. They've done it this way since
  1734." (`edo.hooded`.)
- **Rehearsal**, on the doll on its stand (PEOPLE-21A's `boypuppet-stand` takes the painted puppet's place while it is
  worked): Big Sister's rule, "Where his eyes go, his left hand goes. Watch his head, not me." (his hand to his ear) "His head
  turns. His hand goes up. ...Like that?" "Like that, but as if you meant it." Little Sister's, "When he steps, you stamp. When he
  runs, you run." (stamping) "STAMP. Stamp-stamp-stamp. Run." "...Good. Less joy. He's sad until the end." (`edo.rehearsed`.)
  Each asking for the other's part: "The feet are the small one's. You have hands. Use them." Mom asking for a part: "You're out
  front. Every play needs one person to cry. Go and cry."
- **Mom out front.** Her use of the audience, once both girls have rehearsed: "Places, girls. I'll be out front, where I can
  watch you not being there." She goes round through the gap at the wing wall's end, along the aisle, to the only space left
  in the front row (the `house` floor), and sits back on her heels beside Tatsu. "...You're crying. It hasn't started." "I know
  how it ends. A boy runs home to his mother." "...Here. I always need it." (his towel) "Weren't there three of you?" "There
  were. The other two are at work." "Good. Work's good." (`edo.momSeated`.)
- **The show.** The stage takes the roof hatch's day (PAINT-21D's show state, cross-faded in with the set's lit twins); the doll
  on the rail with Jūbei on his stage clogs at its head and the girls at its left hand and its feet (g.troupe, at PAINT-21D's
  places). The chanter: "A boy, far from home, at evening, and a long road before him." Then three cues, each kept up as a
  caption while it waits for the player, who switches between the girls by their portraits (the doll's left hand is Big
  Sister's, his feet Little Sister's): "The boy hears his mother calling." (Big Sister: his hand to his ear: `edo.cue1`); "He
  runs. He runs. He runs for home." (Little Sister: a run of stamps: `edo.cue2`); "He kneels down at her door." (both, either
  order: the hand to the ground, the feet folded: `edo.cue3`). A part at the wrong cue: the house laughs at a sad play, Jūbei
  hisses "Not yet." (then "Watch his head. Wait for the words."), and the cue comes round again. The other girl's reach for a
  part is Jūbei's hiss of the rule; Mom watches. Then: "And she opens it." The house weeps; Tatsu: "...Best one I've ever seen.
  The boy's feet. You could FEEL him running." Mom (into his towel): "...I thought so too." "Keep the towel. I always bring two."
  The stage goes back to the afternoon, the girls come down out of their black, the doll goes back on its stand, Mom comes
  back round.
- **The troupe.** Jūbei: "You'll do. Both of you. ...Who are you?" Mom: "We have to go west, to Himeji. We'd rather not be asked
  questions on the way." "Then don't go west from Osaka." "We play at Fushimi tomorrow. Up the river, by the Kyoto boat. I need
  carriers." "Get off at Hirakata, and cross by the ferry to the Takatsuki side." "Take the old Yamazaki road west. It goes round
  Osaka," "and nobody on it is looking for three tall women." "Thank you. We'll carry anything you like." (`edo.troupeTaken`:
  the beat.) Little Sister: "Can I be the feet AGAIN? Tomorrow?" "Tomorrow you carry boxes. Feet are for professionals." Big
  Sister: "How long does it take to learn the head and the right hand?" "Thirty years. The first ten, you carry boxes."
- **Wrong tries**: the puppets on their rail (Little Sister: "They're SLEEPING." "They're hanging." "SLEEPING."), the heads (Big
  Sister will not look twice), the chanter's book ("No. Nobody touches a chanter's book."), the boy's head once the girls are
  in black (Jūbei's own place: "Mine? My face shows. You'd need thirty years for that one."), the back door while they are in
  black ("Leave a theater before the play? Never. Not even by the back door.").
- Notes: three operators to a puppet since 1734 and the Inari theatre in Naniwa Shrine's grounds are checked; the black hoods of
  the left-hand and feet operators are the long convention, not checked this round; the play and its cues are the game's own.

```
Cut-Scene: The Kyoto Boat        (edo.boat: needs edo.troupeTaken and edo.sheetRead; edo-boat.js)
```
Played when both are done and Jūbei has his word ("Morning. Hachikenya. Don't be late, and don't be noticed."): straight
after the troupe if the sheet has been read, or when they come back to him from the print shop. Pictures over the stage, as
round twenty's voyage draws the ship by night (the game's own: flat masses, banded skies, the three as small shapes in their
borrowed colours). The card "The Kyoto Boat". Morning at Hachikenya, the long passenger boat by the landing: "Boxes in the boat.
Carriers among the boxes. Nobody sits on the heads." "Twenty-eight passengers, four boatmen and a troupe. I counted. Then I gave
up." "We're SQUASHED. I'm squashed between a box and a man's elbow." Upriver on a long rope, a gang leaning into it on the bank:
"We're being pulled up a river by forty men." "Like a KITE." Hirakata, the food boats alongside (the voice `foodboat`): "Won't
ya stuff some rice? Won't ya swill some sake?" "They're RUDE." "It's the custom. They count the bowls." "Three bowls, for my
carriers. Count them twice. You always do." The ferry to the Takatsuki side, the troupe's boat going on: "Hirakata. You get off
here. The ferry takes you over to the Takatsuki side." "You were good hands, both of you." "Can we come back and be the feet
again?" "You may come back when you are thirty." Mom: "Thank you. For the boat, and the road, and for asking so little." The
map: the portraits up the river path to Hirakata (its picture fades in at the river's turn: the stop named in the journey's
first part, PAINT-21F's), then by the road north to the hills (`g.journey("edo", "osaka", "hills", { segments: [{ to:
"hirakata", sound: "haul", stops: ["hirakata"] }, { to: "hills", sound: "sandals" }] })`). The road north at dusk, the first
rain: "A drop. On my NOSE. ...Two drops." "Rain, and the dark coming. We'll find a roof up there, girls. Up that path."
"North, into the hills, till it's quiet. Gonroku's orders, and Jūbei's road." The card "The hills"; `edo.boated`; the hats on;
the cedar path (`edo-cedars`, `enter`). Skipped, the same.

#### The hints, stage by stage

| Beat | Stage (the facts) | Mom | Big Sister | Little Sister |
| --- | --- | --- | --- | --- |
| #28 `edo.alms` | no paddle (`edo.paddle`) | `hint.edo.alms.mom` | `.bigsis` | `.lilsis` |
| | the line not fed (`edo.fedPilgrims`) | `.mom.2` | `.bigsis.2` | `.lilsis.2` |
| | not vouched for (`edo.vouched`) | `.mom.3` | `.bigsis.3` | `.lilsis.3` |
| #29 `edo.heard` | the custom not heard (`edo.combAsked`) | `hint.edo.heard.mom` | `.bigsis` | `.lilsis` |
| | the chant not heard (`edo.heardShosha`) | `.mom.2` | `.bigsis.2` | `.lilsis.2` |
| | the sheet not caught (`edo.sheetCaught`) | `.mom.3` | `.bigsis.3` | `.lilsis.3` |
| | the comb not given (`edo.combGiven`) | `.mom.4` | `.bigsis.4` | `.lilsis.4` |
| #30 `edo.read` | the marks not seen (`edo.marksSeen`) | `hint.edo.read.mom` | `.bigsis` | `.lilsis` |
| | the paper not laid (`edo.registered`) | `.mom.2` | `.bigsis.2` | `.lilsis.2` |
| | the sheet not read (`edo.sheetRead`) | `.mom.3` | `.bigsis.3` | `.lilsis.3` |
| #31 `edo.troupe` | not hidden (`edo.backstage`) | `hint.edo.troupe.mom` | `.bigsis` | `.lilsis` |
| | the robes not on (`edo.hooded`) | `.mom.2` | `.bigsis.2` | `.lilsis.2` |
| | not rehearsed (`edo.rehearsed`) | `.mom.3` | `.bigsis.3` | `.lilsis.3` |
| | Mom not in her seat (`edo.momSeated`) | `.mom.4` | `.bigsis.4` | `.lilsis.4` |
| | the three cues (`edo.cue1`, `.cue2`, `.cue3`) | `.mom.5` to `.7` | `.bigsis.5` to `.7` | `.lilsis.5` to `.7` |
| | Jūbei not answered (`edo.troupeTaken`) | `.mom.8` | `.bigsis.8` | `.lilsis.8` |
| The Kyoto Boat | (one stage) | `hint.edo.boat.mom` | `.bigsis` | `.lilsis` |

(While two beats are open, #29 and #30, then #30 and #31, each of the three gets the hint of the beat she leads; Little Sister,
who leads neither #29 nor #30, the first open one's; Mom, after #29, #30's.)

### Ledger for this leg

**Things that are carried**

| Thing | Comes from | Who can hold it | Used for |
| --- | --- | --- | --- |
| Rice paddle (`paddle`) | O-Natsu, #28 (the kitchen is hers) | Mom | #28: the pot. Given back, clean, at the supper. |
| Broadsheet (`sheet`) | caught by Big Sister as the yomiuri run, #29 | Big Sister | #30: read aloud by Senzō (its look is the reading after): the voice at Shosha; "every woman in Harima has tried her comb and her pin". For #37's clue chain. |
| Boxwood comb (`comb`) | O-Natsu's, given at the crossroads, #29 | Mom | For #37 (the lock's slits, in Big Sister's hand). |
| O-Natsu's slip (`natsuslip`) | O-Natsu, #29 ("Leave a slip for my boy.") | Mom | For #37: to O-Ume at the women's hall. |
| Blurry print (`blueprint`) | Senzō's first print of the afternoon, #30 | Little Sister | A keepsake ("He's got two noses. I like him BEST."). |
| Peddler's print (`toyamaprint`) | Sōshichi, #24 | Little Sister | Shown to Senzō, #30 (a wrong try, and a kind word). |
| One-mon coin (`mon`) | Kōta, #27 | Little Sister | Not for a broadsheet ("It's a souvenir."). For #37 (the lock's post, in Mom's hand). |
| Hairpin (`kanzashi`) | O-Tami, #22 | Big Sister | Not used here. For #37 (the rabbit's ear, in Little Sister's hand). |

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| "Everybody here has a ladle but us." | the landing | #28: no ladle, no pretending ("And then we'd be lying with a spoon."); the paddle instead. |
| Mom's church suppers for two hundred | #28, her question to O-Natsu | the paddle; "My helpers." |
| O-Natsu's runaway boy, Chōkitton | #28, her tree | #29: the comb, "...a boy, alive and well, calling for his mother!"; her slip for him (#37). |
| "A boy's voice. A language nobody knows." | #29, the chant | #30: the sheet read; Shosha (#37, #38). |
| The sheet's picture: a rabbit running on waves | #30 | #37: the lock. |
| "Every woman in Harima has tried her comb and her pin." | #30 | #37: "Nobody tried a coin." |
| Tatsu following three tall women | #29 | #31: he is in the front row, and Mom weeps into his towel. |
| Three to a puppet | #31 | #37: three hands at once. |
| The road round Osaka (Jūbei's) | #31 | The Kyoto Boat; the hills. |

## Act Six, the third leg: the hills north of Osaka (#32 to #34), and the card "Three days later" / "Akashi"

<!-- SCENES-21B: round twenty's second leg (#25 to #27, now #32 to #34), as built, with round twenty-one's changes. -->
As round twenty built it (`edo-cedars.js`, `edo-storehouse.js`, `edo-chapel.js`, `edo-hills.js`; its section of this
document stands, its puzzles renumbered: #25 Under The Cedars is now #32, #26 Our Father #33, #27 Charcoal, And A Kind Child
#34), with these changes:

- **The way in** is the Kyoto boat now (above), not the voyage's quick passage and "go north": the leg begins on the cedar
  path on `enter` as "The Kyoto Boat" leaves it; #32's beat `edo.hidden` needs `edo.boated` (was `edo.sailed`); LEG_START.hills
  has every fact of Osaka and its pockets (O-Natsu's comb and slip, the broadsheet, the blurry print; the paddle given back).
- **Four days, not three**: Jinsuke's cousin is "at Himeji, four days west" (WRITE-21B's edit), and so are the hints after the
  mirror; the hidden family is told nothing about Shosha.
- **The map**, in the hills (the third leg): Yui and Osaka behind refuse with their own lines ("Yui is a sea and a river
  behind us. We keep going."; "We left Osaka by the river. The magistrates can keep it.").
- **The card** is "Three days later" / "Akashi" (WRITE-21B's edit of round twenty's second word), with Little Sister's line under
  it as built ("Everybody else was going the OTHER way."); then the map: the portraits down out of the hills by Kōriyama and
  west along the shore road past three small pictures (PAINT-21F's), each with its line said over it as the portraits come to
  it (WRITE-21B's): Kōriyama, Little Sister: "A camellia as big as a HOUSE."; Suma, Mom: "A stone for a boy who died young.
  Soba, we can't afford. A prayer, we can." and Big Sister: "A great poet said Suma's flutes weren't worth ten hiki to see. We
  had no hiki." (a stop may say two lines: SCENES-21B's small change to `atlas.js`); Maiko, Big Sister: "Pines, all leaning one
  way. That's the sea wind. I'm NOT saying they know." Then `edo.walked`, and the Akashi shore on `road` (SCENES-21C's
  `edo-akashi`), the fourth leg. Skipped, the same.

| Beat | Puzzle (round twenty's number) | Needs | Sets |
| --- | --- | --- | --- |
| `edo.hidden` | #32 Under The Cedars (#25) | `edo.boated` (was `edo.sailed`) | `edo.hidden` |
| `edo.trusted` | #33 Our Father (#26) | `edo.hidden` | `edo.trusted` |
| `edo.mirror` | #34 Charcoal, And A Kind Child (#27) | `edo.trusted` | `edo.mirror` |
| `edo.walk` | the card "Three days later" / "Akashi" | `edo.mirror` | `edo.walked` |

## Act Six, the hills north of Osaka (#32 to #34; round twenty's #25 to #27), as round twenty built them

<!-- MERGE-21: renumbered in play order; round twenty-one's changes to this leg are in the Osaka part above, under "the third leg". -->

<!-- SCENES-20B: new in round twenty. MERGE-20 joins this with the first and third legs into docs/PUZZLES-japan.md. -->
Twelve days by sea from Yui, and north from Osaka into the hills, in spring rain at dusk: a cedar path, a charcoal-burner's
storehouse, and under it a room dug into the hill where a family keeps the old faith with no priest. The leg begins on the
cedar path, on its mark `enter`, as the voyage leaves it (SCENES-20A's `edo-sail`), and ends when the card "Three days later"
hands on to the castle approach at Himeji (SCENES-20C's `edo-castle`, on `enter`). The design is `briefs/out/edo-design.md`,
sections 3, 5 and 7; the lines are `js/content/lines/edo-b.en.js` and the talks are trees in `js/content/talk/edo-b.js`
(WRITE-20B's; `ids.md` says when each line is said); the beats are in `js/content/acts/edo.js` (act 7); the three scenes are
`js/content/scenes/edo-cedars.js`, `edo-storehouse.js` and `edo-chapel.js`, with what they share in `edo-hills.js` beside
them; the card is `js/content/cutscenes/edo-walk.js`. Play it: `index.html?scene=edo-cedars&lead=lilsis`, then the leg's
start as LEG_START.hills has it (the travel clothes on, the egg and the pink flashlight in Little Sister's pockets, the coin
in Big Sister's): `tests/briefs-out/play-edo-hills.py` sets it up by script.

### The three of them, in the hills

They go together, a party of three, from the path to the room and back: whoever leads, the other two come too. Two
moments split them. At dusk Little Sister goes in by the storehouse's back window alone, and Mom and Big Sister wait on the
path until she lifts the bar. In the morning the constable's man is coming up the path, and Mom is the one he is looking
for: she will not lie to him, so she must not be asked. From O-Rin's warning until he has gone the two girls go together,
and Mom goes on her own (`edo-hills.js` partyOf); a click on another one's portrait opens the map of Japan with her portrait
in the hills, and a click on her there drops into her scene.

**The hats.** Out on the path, under the rain, the travel hats are on (PEOPLE-20's outfit `edo`); indoors, in the
storehouse and the room, they hang on their backs (`edo-hatback`). Little Sister sleeps flat on the mats (`edo-lying`), and
Mom, with the grandmother's mirror held up in the sun, is in `edo-mirror`; the card puts the hats back on for the road.

**The times.** One evening, one night, one morning, told by the facts: dusk on the path (until they go down the ladder:
`edo.hidden`), the evening below (#33, until `edo.trusted`), the night (their own talks with Sei, Jinsuke and O-Rin, and
sleep), the morning (O-Rin's warning, `edo.watch`, until the constable has gone, `edo.constableGone`), and the sun on the
ladder after. It rains from the evening they come until he goes down the path with the egg (the rain on the path, its
drips from the eaves and puddles on the treads; in the storehouse the rain loud on the thatch, seen in the high window and,
when the door stands open, in the doorway); then the sun comes down the open trapdoor.

**The constable's way up the path** (#34) is a count of beats, not a timer: he is at the foot of the steps when O-Rin
sees him, climbs a step nearer each time one of the two things upstairs is done (the sacks, the pink light), and once all
three things are done (Mom below too) he climbs the last steps and knocks. Each step is seen: the storehouse looks out at
the path for a moment (the lead stays where she was), and he yawns. A look out of the door before the room is ready shows
him where he is.

### Puzzle structure

```
                 (the voyage: SCENES-20A's "The Uttermost Parts"; the card "Twelve days later", Osaka)
                                        |
                 #32 Under The Cedars (Little Sister; the path, the storehouse)
                     the door barred and nobody answering; calling out; the pipe in the hill: "The ground is PRAYING."
                     the high window: Mom lifts her; alone on the sacks; the bar
                     the mat with light at its edge: a trapdoor; "We should knock."; the light goes out, and comes back
                                        |   edo.hidden
                 #33 Our Father (Mom, then Little Sister; the room under the storehouse; a talk)
                     "We are charcoal-burners."; true things, and nothing asked; prayers, out loud
                     "Ten ni mashimasu..."; the altar; John 1:5 given and said back; O-Rin laughs once
                                        |   edo.trusted
                 the night: their own talks (the mirror, the cousin at Himeji, a light with no fire); sleep
                                        |
                 #34 Charcoal, And A Kind Child (all three; the room, the storehouse)
                     O-Rin's warning;  the sacks over the mat  |  the pink light off  |  Mom below
                     (any order: a step up the path for each of the first two; all three: the knock)
                     the constable let in; true answers; the egg: "Nothing here but charcoal and a kind child."
                                        |   edo.constableGone
                     the sun on the ladder: the grandmother's mirror, the cross in its light on the wall;
                     the mirror and the trowel to Mom; the castle's two stories: "That's a door."
                                        |   edo.mirror
                 Card: Three days later / Himeji ("Everybody else was going the OTHER way.")   edo.walked
                                        |
                 (the third leg: SCENES-20C's #39 Eight At The Gate)
```

The beats (`js/content/acts/edo.js`), each with its fact: `edo.hidden` (#32: lead Little Sister; it needs `edo.sailed`),
`edo.trusted` (#33: Mom and Little Sister), `edo.mirror` (#34: the family) and the card `edo.walk` (`edo.walked`). The
scenes' own facts the staged hints read: `edo.pipeHeard` and `edo.unbarred` (#32); `edo.sacksHid`, `edo.pinkOff` and
`edo.momBelow` (#34); and, with the change asked of MERGE-20 (ready.md), `edo.watch` and `edo.constableGone`.

### Location layout

Three places, one painting each, in the hills place of the map of Japan (the second leg: the map refuses Yui behind them,
"Twelve days by sea."). The path and the storehouse are joined by its door (once the bar is up); the storehouse and the
room by the trapdoor and its ladder. No way out at the edges.

```
THE CEDAR PATH (edo-cedars): dusk, spring rain; the steps climb between the cedars to the storehouse
+------------------------------------------------------------------------------------+
|  the RAIN, the CEDARS (trunk after trunk, the crowns lost above the frame), the MIST  |
|                  the STOREHOUSE, its thatched EAVES dripping   the high WINDOW (its   |
|                  the DOOR (barred inside), the line of LIGHT   back; lit when the     |
|                  under its floor                               lamp is)  the bamboo   |
|                                                                PIPE in the hill      |
|  the stone FIGURE in its bib       the stone STEPS (their bottom treads)  the KILN    |
|  Here: the three of them, up the steps from Osaka                                     |
+------------------------------------------------------------------------------------+

INSIDE THE STOREHOUSE (edo-storehouse): small, dark boards, the rain loud on the thatch
+------------------------------------------------------------------------------------+
|  the paper LANTERN      TOOLS on pegs     the small high WINDOW,   the straw ROPE     |
|  on its hook            (saw, rake)       SACKS under it            the DOOR, its BAR  |
|  sacks along the left wall                                         the BASKETS        |
|                 the straw MAT over the TRAPDOOR, light between the FLOORBOARDS        |
|  In the morning: O-Rin by the lantern, Jinsuke by the door; the constable inside it   |
+------------------------------------------------------------------------------------+

THE ROOM UNDER THE STOREHOUSE (edo-chapel): dug into the hill, timber-propped, three oil lamps
+------------------------------------------------------------------------------------+
|  the BEAMS and the boards of the storehouse floor overhead; the TRAPDOOR in its hatch |
|  a LAMP     the LADDER    the earth WALL   the closet ALTAR (shut; open: the white     |
|  on its                                    KANNON with a child, the folded CALENDAR,   |
|  ledge                                     the BOWL of water); the LAMP on its stand;  |
|  the timber PROPS          the MATS        the MIRROR on its STAND; a LAMP in a niche  |
|  the BASKET                                GRANDMOTHER SEI, kneeling   JINSUKE, O-RIN |
|  In the morning: her pink FLASHLIGHT on the mats; after the constable, the SUN on them |
|  the water JAR, a charcoal SACK                                                       |
+------------------------------------------------------------------------------------+
```

### Puzzles, as built

```
Puzzle #32: Under The Cedars        (Act Six · Lead: Little Sister · the cedar path, the storehouse)
```
Coming up the path the first time: a temple bell far off, the lamp lit in the storehouse's high window, and out (Big Sister:
"The lamp went out when we came. I saw it go."). A thin line of lamplight under the storehouse's floor.

- **The door** is barred from inside. A use knocks ("I knocked, as nicely as I know how. Whoever's in there knows how to be
  quiet."); the next calls out ("Hello? ...It's gone quiet. I've frightened somebody. I'm sorry."; Little Sister: "HELLO.
  ...It stopped praying. Oops."): the line of light under the floor goes out for a moment, and comes back. Turn and turn
  about, as long as anyone tries.
- **The pipe** in the hillside ("Listen at"): Little Sister: "The ground is PRAYING." (each has her own: Mom's "Someone's
  saying a prayer in there, low."). `edo.pipeHeard`.
- **The high window** at the back: Mom ("I could reach it. I could not go through it. My shoulders are a civilized width.")
  and Big Sister refuse it, and point at her. Little Sister: "Mommy, LIFT me. I'll go through and open the door. I fit." Mom
  comes over and lifts her; she climbs onto the sill (PEOPLE-20's `climb`): Mom, "Careful of the lamp, sweetheart. And of
  whoever put it out." Through, and down onto the sacks inside, alone: "I'm IN. I landed on something soft. ...It's bags.
  Bags of black." (Big Sister, outside: "She's in. She's always in. It's her whole career."). She hops down.
- **Alone in the storehouse**, everything is hers to look at; the mat she leaves ("A mat. It's got a nightlight UNDER it.").
  The door (or the bar): "I lifted the stick. It's HEAVY. ...Got it. Come in." The bar up, the door open, `edo.unbarred`;
  Mom and Big Sister come in out of the rain. (Outside, the door's look is now "Unbarred, by a seven-year-old, from inside.
  I'm writing that down.")
- **The mat**, with light at its edge (any of them): "A trapdoor. ...Girls, we're in someone's house." Then: Big Sister, "We
  should not open that." Mom, "No. We should knock." Little Sister, "Knock on a FLOOR?" Mom, "It's still a door, sweetheart.
  Manners apply." (`edo.matMoved`; Big Sister's own line says the first of them, so it is not said twice.)
- **The knock** (the trapdoor's use): three knocks on the boards; the light between them goes out. Little Sister: "It went
  OUT." Big Sister: "...And back. Someone down there decided something." Mom: "Then we go down slowly, and we go down kind."
  (`edo.knocked`)
- **Down** (the trapdoor again): the lead's own line ("We knocked. We were answered. Down we go, slowly."), the trapdoor
  open, `edo.hidden`, and the room.

Wrong tries as the design has them: the barred door, calling out, the stone figure (Big Sister will not touch it; Little
Sister says good evening to it), the rain (Little Sister, face up: "It's raining in JAPAN."); and every other thing's own
refusal for each of the three.

```
Puzzle #33: Our Father        (Act Six · Lead: Mom, then Little Sister · the room under the storehouse · a talk)
```
At the ladder's foot: Grandmother Sei kneeling by her mirror, Jinsuke with his arms out in front of his daughter (his
`shield`), O-Rin peeking round him. Jinsuke: "We are charcoal-burners. This is where we keep the charcoal dry." Big Sister:
"...It's a room with lamps and mats." Jinsuke: "Dry charcoal likes a lamp." Mom: "Then we've come down into your charcoal
uninvited, and I'm sorry for it." (`edo.roomMet`). Then the room is the player's: the shut cupboard ("A cupboard. New doors
on old hinges. Somebody replaced one and kept the other."), the mats, the lamps, the mirror on its stand, O-Rin's hands. The
ladder is not yet ("I'm going UP. Watch me go up." Mom: "Up to the storehouse. In a moment, darling.").

A word with any of the three hosts is the room's talk (`roomTree`), and once begun it is talked through: Mom's three true
openings ("We're strangers, we're wet, and we mean you no harm. All three are true." Sei: "Strangers, yes. Wet, yes. The
third I will see."), the wrong foot ("What is this room?" Jinsuke: "Charcoal." Mom: "...I shouldn't have asked. I withdraw
the question."), Big Sister's hinges and Little Sister's hands (the clues), and the lever, one for each lead, always Little
Sister praying: Mom, "Prayers, girls. Then sleep." Little Sister, "Out loud?" Mom, "...Yes, sweetheart. Out loud." She folds
her hands: "'...Our Father which art in heaven, Hallowed be thy name.'" A silence; the grandmother, very low: "...Ten ni
mashimasu..." Big Sister: "Which art in heaven. The same words. It's the same prayer." Mom: "...Yes. It is." Sei: "Jinsuke.
The doors." "Mother--" "A child said it out loud in my house. The doors." She gets up and opens the altar herself
(`edo.prayed`, `edo.altarOpen`). "That's Mary. She has a BABY." Sei: "To anyone who asks, she is Kannon-sama: the one who
hears. To us, she is Maria." Then every question (the calendar, the water and O-Rin's baptism, no priest since 1644, the six
taken in Osaka, the plan east among the pilgrims, O-Rin's whisper), and Mom's gift: "'And the light shineth in darkness; and
the darkness comprehended it not.'" "Again." She says it again, and Sei says it after her (`edo.verse`). Little Sister's
raccoon; O-Rin laughs out loud once and covers her mouth (`edo.laughed`); Sei: "...Leave it, Jinsuke. I had forgotten the
sound." "Sleep, girls. We're under a hill, in a church, with friends." They settle on the mats (`edo.trusted`).

**The night.** Each of them may talk with each host (their own trees): Sei's mirror ("It was my mother's. Its face has not
seen the sun in my lifetime." "In the morning, when the sun comes down the ladder, I will show you why."), Jinsuke's cousin
at Himeji ("He has my trowel, or I his."), his "Truth, and not much of it."; O-Rin and a light with no fire in it (Little
Sister's flashlight comes on in O-Rin's hands, pink). The ladder goes up now: the storehouse's lantern lit again, the lamp
in its window seen from the path. The mats: sleep. Little Sister leaves her flashlight on, on the mats by her, for O-Rin
(out of her pockets: `edo.lightLeft`).

```
Puzzle #34: Charcoal, And A Kind Child        (Act Six · Leads: all three · the room, the storehouse)
```
Morning. O-Rin comes down the ladder white: "Father. A man on the path. Alone. The stick with no tassel." Jinsuke: a
constable's man; he cannot take anyone without an order; he can look; three foreign women from the river mouth, and anyone
not living where their temple says. Mom: "Then I'm the one he's looking for, and I won't lie to him. So he mustn't see me."
Big Sister: "Not up here, Mother. He'll look up here. Down, with Grandmother Sei." Little Sister: "I'll do the talking. I'm
GOOD at talking to men with sticks." Jinsuke: "The mat. The sacks. And whatever is making the floor pink." (`edo.watch`;
Mom below, `edo.momBelow`). Jinsuke and O-Rin go up: he keeps the door, she watches by the lantern.

Three things, in any order:
- **The sacks.** In the storehouse, the sacks (or the mat aside, or O-Rin), with Big Sister there: the mat back over the
  trapdoor and the sacks over the mat. "How many sacks go over a charcoal-burner's mat? Eleven. Everybody knows that."
  O-Rin: "...Do they?" "They do now. Eleven. Help me with the last four." (`edo.sacksHid`.) The trapdoor is under them from
  now on: going up or down, O-Rin shifts them and puts them back: "...Eleven. Again." (a line of mine).
- **The pink light.** Pink stripes between the floorboards (Little Sister: "Pink stripes. ...Oops. That's MINE."). Up there,
  Mom and Big Sister cannot turn it off; Little Sister's use: "I can't reach it through the floor. I'll go DOWN. Sorry,
  light." Down, to it on the mats: "Sorry, light." Off, and back in her pockets (`edo.pinkOff`). Below, Mom and Big Sister
  leave it to her ("I'll let her turn it off. It's hers, and she'll want to say goodbye to it.").
- **Mom below.** She stays with the grandmother (who prays, very low); each of them, kneeling with Sei, says the plan again.

Each of the first two done, the constable climbs a step nearer (a look at the path; he yawns). All three, he knocks; a girl
in the storehouse answers at once, a girl below hears it and goes up to answer; Mom below does not ("No. If he asks me,
I'll tell him. So he mustn't ask me.").

Wrong tries: **Mom up the ladder** (allowed: Big Sister, "Not up here, Mother. He'll look up here." The hint's third stage is
for this; and once he is at the door the ladder is refused her: "No. If he asks me, I'll tell him."); **the door before the
room is ready** (a look out through the crack at him on his step: Mom, "A man coming up the path, wet to the skin, with a
stick in his belt. Alone." / "Inside, girls. Places."; then Jinsuke's reason, by what is still wrong: "The mat is off and
the sacks are not on it. He will see the floor has a door." / "The floor is pink. Charcoal is not pink. Whatever is lit
below, put it out." / "Your mother is up here. He will ask her, and you say she does not lie. Down."); Jinsuke asked
before (his reason); **Big Sister answering for Mom** (the tree's wrong foot: "If you're asking about our mother, she's...
not available." Jinsuke: "Do not help." Isuke: "Was I asking about a mother?").

**The constable** (`isukeTree`). "Morning. ...Pardon. Long night, and a wet one." Jinsuke opens the door (it stands open
while he is in, the rain in the doorway); Isuke comes in out of the rain to his place, dripping; Jinsuke steps between him
and the girls. "Three foreign women, seen at the river mouth. Tall. In hats." "And anybody living where the temple register
doesn't say." "Who are these two?" Jinsuke: "Guests." "Guests. ...Where from?" Big Sister: "The sea." "The sea?" "Most
things come from the sea, eventually." "...I'm writing that down. It's the best answer I've had all week." (her east, her
height; once her answers are used up, "He's asking questions. I'm answering them. Truthfully. It's going oddly well.").
Little Sister (who first sizes him up: "He's hungry. I can TELL. His tummy said so."): the hats, the church, the yawns ("Five.
I did one on the path. ...Don't tell the magistrate."), the boots, and the egg, in both hands: "You're hungry. Here. It's a
good egg. I was going to hatch it." "...Nobody's given me anything on duty. Not once. Not a radish." "It's warm. I kept it
warm since Nevada. That's a long way to keep an egg." "I'll carry it careful." (`edo.eggGiven`; with no egg, the rest of
Kihei's sushi: `edo.sushiGiven`.) "Charcoal. Sacks of it. Two guests, from the sea." "Nothing here but charcoal and a kind
child." "I'll tell them nothing. It's what I'm best at." "Arigatō, wet man. Mind the steps. They're PUDDLES." "...Arigatō
yourself." He goes out with the egg in both hands, and down the path in the rain (seen). (`edo.constableGone`; the rain
stops.) Big Sister: "He wrote down 'the sea'. He underlined it." Jinsuke: "...Come down. My mother has something for yours,
and the sun is on the ladder."

**The mirror.** Down, the sun is on the mats in a square (each has a look and a try: "Sun needs something to bounce off.
There's a mirror on that stand. Not mine."). A word with the grandmother (`mirrorTree`, no choices): "Now. Stand there, by
the wall. Jinsuke, the trapdoor wide." "In the dark we keep it. In the light it speaks." She takes the mirror off its stand,
stands in the sun and turns its light onto the earth wall (ENGINE-20's `mirror` light, `cross-sei`): in the bright patch, a
cross (`edo.crossShown`). "There's a CROSS on the wall. Made of light." Big Sister's physics, and the one thing she has no
physics for. "My mother said: nobody can take a thing off you that is only there in the light." The gift: "Take it where it
can be held up in the light." "I can't take your mother's mirror." "You are not taking it. I am sending it. It is different,
and I am older." "...Then I'll carry it, and I'll find it some sun." The mirror is Mom's, and she holds it up where the
grandmother stood: the cross is on the wall again, from her hands (`edo.mirrorUp`, `cross-mom`). Jinsuke's trowel for his
cousin Tomezō, into her sash. The castle's two stories: a tile with a cross on the gate; a lady at the top of the keep who
asks people why, and is kind to the honest; "And some nights there is a light up there nobody lit." Big Sister: "That's a
door." Mom: "Then we go to Himeji." The goodbyes ("...Goodbye. Out loud."). `edo.mirror`.

Then the room is theirs for a moment: Mom stays where she is holding the mirror up (the scene's `still`), and the wall's
look is the cross ("A cross, in the light, on the wall. And nowhere on the mirror."). The ladder: the card.

```
Card: Three days later
```
The hats on; the stage goes dark; the card, "Three days later" / "Himeji", with Little Sister's line under it: "Everybody
else was going the OTHER way."; the map of Japan, the family's portraits along the road west from the hills to Himeji in
straw sandals (`g.journey`); `edo.walked`; the castle approach, on its mark `enter`, with no era card. (The design's "the
road's own little figures going east with their ladles" is not drawn: the journey has the family's portraits only.)

#### The hints, stage by stage

| Beat | Stage (the facts) | Mom | Big Sister | Little Sister |
| --- | --- | --- | --- | --- |
| #32 | the pipe not heard | `hint.edo.hidden.mom` | `.bigsis` | `.lilsis` |
| | the door barred | `.mom.2` | `.bigsis.2` | `.lilsis.2` |
| | the mat (unbarred) | `.mom.3` | `.bigsis.3` | `.lilsis.3` |
| #33 | (one stage) | `hint.edo.trusted.mom` | `.bigsis` | `.lilsis` |
| #34 | the night (no `edo.watch`) | `hint.edo.mirror.mom.0` (new) | `.bigsis.0` | `.lilsis.0` |
| | the sacks | `hint.edo.mirror.mom` | `.bigsis` | `.lilsis` |
| | the pink light | `.mom.2` | `.bigsis.2` | `.lilsis.2` |
| | Mom not below | `.mom.3` | `.bigsis.3` | `.lilsis.3` |
| | he is at the door / in | `.mom.4` | `.bigsis.4` | `.lilsis.4` |
| | he has gone (`edo.constableGone`) | `.mom.5` (new) | `.bigsis.5` | `.lilsis.5` |
| the card | after the mirror (the beat `edo.walk`) | `hint.edo.mirror.mom.6` (new) | `.bigsis.6` | `.lilsis.6` |

### Ledger for this leg

**Things that are carried**

| Thing | Comes from | Who can hold it | Used for |
| --- | --- | --- | --- |
| One warm egg | Darlene, out back (Act Four #11): Little Sister's since Nevada | Little Sister | #34: given to the constable's man, freely ("It's a good egg. I was going to hatch it."). He goes down the path with it in both hands. |
| Box of sushi | Kihei's (#23) | whoever the first leg left it with | #34, only if there were no egg: the rest of it, to the constable ("It's fish man's sushi. It's SQUARE."). The voyage eats it (SCENES-20A), so in the game as played the egg is always given. |
| Pink flashlight | Little Sister's own (Act Three) | Little Sister | The night: on in O-Rin's hands (a light with no fire). #34: left on, on the mats, for O-Rin: its light up between the floorboards. "Sorry, light.": off, and back in her pockets, for #40 (the warden). |
| Bronze mirror | Grandmother Sei's mother's, on its stand in the closet altar | Mom | #34's end: the cross in its light on the earth wall; sent with Mom, "where it can be held up in the light". For #41. |
| Plasterer's trowel | Jinsuke's cousin Tomezō's ("He has my trowel, or I his.") | Mom (in her sash) | For #39: give it back to Tomezō, and say Jinsuke is well. |
| Silver coin | Big Sister's, from Act Four | Big Sister | Not used here. For the end of the act. |

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| The warm egg, kept warm since Nevada | Act Four #11 ("It's MINE to keep warm.") | #34: "He was hungrier than it was ready to hatch." |
| "I FIT" | Acts Three and Four | #32: the storehouse's back window, a cupboard door's size: "I'm IN." |
| Knocking at doors, as manners | Mom, everywhere | #32: "It's still a door, sweetheart. Manners apply." A knock on a trapdoor is answered. |
| Little Sister's prayers out loud | The family's bedtime; O-Rin "has never said her prayers above a whisper" | #33: "Our Father..." answered with "Ten ni mashimasu..."; the night: O-Rin's prayer, a little louder; the goodbye: "...Goodbye. Out loud." |
| The grandmother's mirror ("Its face has not seen the sun in my lifetime.") | #33, on its stand; the night, her tree | #34's end: the cross in its light. #41: the door in the keep's sunset. |
| The cousin at Himeji, the trowel | The night, Jinsuke's tree | #34's end: the trowel; #39: Tomezō. |
| "Everybody else is going the other way." | #33, Big Sister on the pilgrims | The card: "Everybody else was going the OTHER way." |
| A light nobody lit, at the top of a building nobody may climb | #34's end, the castle's stories | #40 and #41 (the third leg). |
| Little Sister's pink flashlight | Act Three; the night here (O-Rin) | #40: lent to the warden. |

## Act Six, the road west: Akashi, Himeji town and the women's hall (#35 to #38, "The next day" and "Mind The Fire")

The fifth stretch of the act, as built in round twenty-one (SCENES-21C): the Akashi shore in the afternoon, three days out
of the hills; the next day, Himeji town at midday, the foot of Mount Shosha and its women's hall at sunset; the walk back
in the dark; and, the next day, round twenty's castle and keep (#39 to #41, as built, entered now from the town). The
lead joins this part with SCENES-21A's and SCENES-21B's into `docs/PUZZLES-japan.md`. The lines are WRITE-21B's
(`js/content/lines/edo-d.en.js`), quoted here as the game says them, in the order it says them; the talks are WRITE-21B's
trees and lists (`js/content/talk/edo-d.js`), staged by the scenes (`js/content/scenes/edo-akashi.js`, `edo-town.js`,
`edo-shosha.js`, `edo-lock.js` (the lock up close), `edo-hall.js`, and what they share, `edo-west.js`) and the cut-scenes
(`js/content/cutscenes/edo-walk2.js`, `edo-night.js`; and one new line in round twenty's `edo-step.js`).

### Puzzle structure

```
          (from the hills: "Three days later" / "Akashi", the walk card: SCENES-21B's edo-walk)
                                        |
         #35 The Ladle (Little Sister, with Mom and Big Sister; the Akashi shore)
             O-Fusa's ladle out in the shallows with an octopus in it; boots are for water; "a tako
             lets go of nothing, except for a crab"; Mom's crab from under the rocks; the swap;
             the ladle back: O-Fusa's slip for Shosha, a penny for luck (edo.ladleBack)
             (and O-Sato's news, any time: "it opens to what a ship gives its lady": edo.riddle)
                                        |
         Card: The next day / Himeji  (edo.inHimeji)
                                        |
         #36 Supper For A Voice (each her own part; Himeji town)
             Little Sister: O-Kiku's first day, hand in hand, "mother"  (edo.kikuIn)
             Big Sister: O-Shizu draws the way to Shosha               (edo.knowWay)
             Mom: O-Tane's kitchen, rice balls in order                 (edo.riceballs)
             -> the map to Shosha (edo.supperMade)
                                        |
         #37 What A Ship Gives Its Lady (all three at once; the foot of Mount Shosha, the lock up close)
             the mountain refuses; O-Ume and the riddle; the lock; Big Sister's list from the ship:
             a comb, a pin, a coin; handed round to the right hands; the pin in the ear (held), the
             coin on the post (held), the comb in the slits: it chirps (edo.hallOpen)
                                        |
         #38 A Small Door At Sunset (Mom, then all; inside the women's hall)
             the bars of light climb to the hum: the Son's voice; the talk; more light, more door
             (the pink flashlight); a rice ball through the door (edo.sonFed); "Hold hands."; the
             sun goes, Isaiah 49:15
                                        |
         Cut-scene: Mind The Fire (the lantern; the fields; the clappers, gate to gate; O-Tane's door;
         the dark)  ->  card: "The next day"  ->  the castle approach (edo.nightDone)
                                        |
         #39 Eight At The Gate / #40 A Light That Needs No Fire / #41 The Lady Of The Keep
         (round twenty's #28-#30, as built)  ->  Hold Hands ("My brother SAID." first)
```

Goal of the stretch: **find the voice at Shosha before the sun goes down, and feed it.** The stretch begins at
`LEG_START.akashi` (`js/content/scenes/edo-common.js`): the Akashi shore at `road`, the three of them in O-Tami's travel
clothes with their hats on; Mom carrying the spare car key, O-Natsu's comb and her slip for Chōkichi, the bronze mirror
and Jinsuke's trowel; Big Sister Dad's pencil, her note (the Funadama's list from the ship), the Son's coin, O-Tami's
hairpin and the broadsheet; Little Sister two pennies, the one-mon coin, her pink flashlight, Sōshichi's print and the
spoiled blue one.

The beats (`js/content/acts/edo.js`), each with the fact it makes true: `edo.ladle` (#35: `edo.ladleBack`; it needs
`edo.walked`), `edo.walk2` (the card: `edo.inHimeji`), `edo.supper` (#36: `edo.supperMade`), `edo.hall` (#37:
`edo.hallOpen`), `edo.son` (#38: `edo.sonFed`), `edo.night` (the cut-scene: `edo.nightDone`); round twenty's
`edo.inside` (#39) now needs `edo.night`. Each puzzle's hint follows how far it has got, for each of the three (the facts
the scenes set for it; WRITE-21B's `hintFor`):

| Puzzle | Stage | The fact that moves it on | Mom's hint at that stage |
| --- | --- | --- | --- |
| #35 | O-Fusa not met | `edo.fusaMet` | "That little girl's lost something. Your sister speaks fluent nine-year-old." |
| #35 | nobody in the water | `edo.waded` | "The ladle's out in the shallows, and only one of us is wearing boots." |
| #35 | the octopus holding on | `edo.crabClue` | "It's holding on. The old fisherman knows octopus. Ask what it lets go for." |
| #35 | no crab | `edo.crab` | "A crab, he says. Under the rocks. I'll do that part. I've done bath time." |
| #35 | the crab not swapped | `edo.ladleFree` | "The crab goes to your sister, and she holds it out to the octopus." |
| #35 | the ladle not given back | `edo.ladleBack` | "The ladle's free. Back to its owner, before her group goes." |
| #35 | O-Sato not asked | `edo.riddle` | "The two women on the road come from near Himeji. Ask them about Shosha." |
| #35 | done | (the road west) | "West, girls. Himeji's a day on, and the voice comes at sunset." |
| #36 | O-Kiku outside | `edo.kikuIn` | "That little girl needs someone her own size to go in with. Your sister." |
| #36 | the way not known | `edo.knowWay` | "The teacher knows the way to Shosha. Your sister should ask her. They'll get on." |
| #36 | no kitchen | `edo.kitchenLent` | "Supper for the walk, and one for the voice. O-Tane's kitchen, if I ask nicely." |
| #36 | the kitchen, no rice balls | `edo.riceballs` | "Water first, then salt, then rice. The pickle last, and then the cloth." |
| #36 | done | (the map to Shosha) | "The way's drawn, and supper's made. Shosha, girls, before the sun's low." |
| #37 | O-Ume not met | `edo.oumeMet` | "The old woman by the hut keeps the hall. Ask her about the lock." |
| #37 | the lock not seen | `edo.lockSeen` | "Look at the lock itself, close up. Every part of it." |
| #37 | the list not read | `edo.listRead` | "What a ship gives its lady. Your sister wrote it down on the ship. Ask her." |
| #37 | the things in the wrong hands | the pin with Little Sister, the coin with Mom, the comb with Big Sister | "The ear wants small fingers, the post a strong wrist, the comb a steady hand." |
| #37 | in the right hands | `edo.earHeld` (not saved) | "Your sister, the pin, the rabbit's ear. She holds it while we do the rest." |
| #37 | the ear held | `edo.postHeld` (not saved) | "The coin on the square post, and turn. That's my wrist. I hold it." |
| #37 | the ear and the post held | `edo.hallOpen` | "The comb in the slits, steady. That's your sister's hand." |
| #38 | the voice not heard | `edo.sonHeard` | "Inside, where the sun falls on the wall. We sit, and we listen." |
| #38 | a door the size of a coin | `edo.doorWide` | "It's the size of a coin. More light, more door. Your sister's light." |
| #38 | a hand wide, not fed | `edo.sonFed` | "A door the size of my hand, and a rice ball in my sleeve. Supper." |
| #38 | fed | `edo.holdHands` | "Tell him where we're going tomorrow. Before the sun goes." |

### Location layout

Four places on the act's map (`akashi`, `himeji`, `shosha` with the hall inside it) and the lock up close. Akashi leads
west only by the card, once the ladle is back; the town leads to Shosha by the map, once the way is known and supper made
(and back up the lane north to the castle the next day only); Shosha's road back refuses ("Not now, darling. The sun's
going down. That's the point of being here."); the hall is entered through the open doors; the night ends at the castle.

```
THE AKASHI SHORE (edo-akashi): afternoon
+------------------------------------------------------------------------------------+
| the SKY        AWAJI, long and low across the STRAIT              the CASTLE (four  |
|                                                                   turrets, no keep) |
| the PILGRIM BOAT from Awa, sail down        the octopus POTS on their LINES, floats |
|   the two Awa pilgrims wading in, ladles up      the LADLE, floating, an octopus in   |
|   (their BANNER)              the SHALLOWS (Little Sister's alone, in her boots)    |
| HEITA's boat and TUB (old Heita, sitting)                         the ROCKS (crabs) |
| O-FUSA in tears on the SAND, her group's LEADER         the two shore PINES         |
| the ROAD east  <- O-SATO and her sister-in-law, Ise-bound, behind the pines ->  west |
|   (a komusō passes now and then)                                       Here: road   |
+------------------------------------------------------------------------------------+

HIMEJI TOWN (edo-town): Watamachi at midday
+------------------------------------------------------------------------------------+
| the KEEP, white, above the roofs; a kite circling                                   |
| the WRITING SCHOOL (O-SHIZU, two PUPILS,     O-TANE's house: the NOREN; the KITCHEN |
|   the DESKS: a floor of its own, up the       DOOR; behind it the WELL, the BUCKET,  |
|   STEP STONE)                                 the SALT jar, the PLUM jar, the RICE    |
| O-KIKU outside it, in her best clothes        POT, the PICKLE tub, the CLOTH           |
| the COTTON office, the paper-note office      TŌBEI's hut (sandals, sweets)           |
| the bales; the komusō playing                 the WARD GATE; the LANE north (castle) |
| the STREET                                                     Here: east (highway) |
+------------------------------------------------------------------------------------+

THE FOOT OF MOUNT SHOSHA (edo-shosha): late afternoon, then the red light of the sunset
+------------------------------------------------------------------------------------+
| the SKY; the MOUNTAIN in pines and maples; the PATH up (the east path)              |
| the women's HALL: its double DOORS, SLIPS pasted round them; on the hasp the LOCK   |
|   (a rabbit over waves); a rice ball on a leaf on the STEP; the LATTICE at its side  |
| the small STONE, RYŌKAI on a step by it         the BENCH: Grandmother TOME, a WIFE, |
| O-UME by her hut                                 a GIRL, waiting; the HEAP of combs  |
| the PINE                                                          Here: road (east) |
+------------------------------------------------------------------------------------+

THE LOCK, UP CLOSE (edo-lock): the rabbit running over three waves
  the EAR (and its HOLE), the WAVES (the middle one a hair loose; under it the square POST),
  the BACK (a carved line: the SLITS once the coin turns), the BOLT through the hasp; the three
  hands drawn as they hold (g.hand, LOCK_HANDS)

INSIDE THE WOMEN'S HALL (edo-hall): sunset
+------------------------------------------------------------------------------------+
| the CEILING; the SLIPS, thousands, on the back wall and the beams                   |
| the west LATTICE (Ryōkai's face in it,   the CABINET (Kannon), the LAMP, the       |
|   outside, once the hall is open)          INCENSE, the FLOWERS, the POSTS          |
| O-UME kneeling by the door                the MATS          the east WALL: the BARS |
|                                                             of red light climbing;  |
| the women's writing DESK (front)                            the HUM, and the DOOR   |
| the DOORWAY                                                       Here: door        |
+------------------------------------------------------------------------------------+
```

### Cut-scenes and puzzles

```
Puzzle #35: The Ladle        (Act Six · Lead: Little Sister, with Mom and Big Sister · the Akashi shore)
Needs:        the walk out of the hills (edo.walked)
Setup:        They come along the road onto the sand as a pilgrim boat from Awa unloads; two of its pilgrims wade in,
              ladles held up dry ("Mind the pots! Mind the POTS. That's somebody's supper." "Ladles up! Whoever drops a
              ladle walks to Ise hungry."). Little Sister: "The SEA again. And a boat full of spoons." Big Sister:
              "Pilgrims, wading in from that boat. Every one holding a ladle up, dry." Mom: "All but one. Look, girls.
              That little one's crying." The two come ashore and stand with their leader; O-Fusa, nine, sits on the sand.
Wrong tries:  The road west (before the ladle)  -> Mom: "Not yet. Not with that little girl crying on the sand." Big Sister:
                                                   "West is Himeji, and it'll keep. That girl's ladle won't." Little Sister:
                                                   "Not till the girl gets her LADLE back."
              The road east                     -> "Three days of that. NO." (and Mom's, Big Sister's own)
              The ladle, from the sand          -> Mom: "It's past the floats. I'd be in up to my sash, and so would the
                                                   kimono." Big Sister: "In sandals, from the shore, everything out there is
                                                   out of reach."
              The shallows (Mom, Big Sister)    -> "Not in sandals and silk. Not if I can help it." / "I put a toe in. It's
                                                   the Inland Sea, and it's cold, and it's in my sandal." (the shallows are a
                                                   part of the floor for Little Sister alone: the others walk to its edge)
              The octopus, pulled again         -> "I pulled. It pulled back. It's WINNING."
              The rocks (Big Sister; Little     -> "I'm not putting my hand under a rock. I've read about what's under
              Sister; Mom before the clue)         rocks." / "I tried. They go SIDEWAYS. I can't do sideways." / "There's
                                                   something sideways under there. I'll let it be, for now."
              The castle (Big Sister)           -> "Four turrets and no keep. Japan has a thing about castles with no tops."
              The pots (Little Sister)          -> "The octopus goes IN because it likes a cozy hole. Then it's supper."
              The strait (Big Sister)           -> "Two and a half miles of sea to that island, and a tide like a river."
Solution:     (1) O-Fusa (a talk, each of them her own way in): Little Sister's "I'll get it. I'm good at water." "You
              can't. You'll get wet. Pilgrims don't get wet." "I won't get wet. I've got BOOTS." "...What are boots?"; Mom's
              "Are you all right, sweetheart? What can we do?" ("Don't pat me. I'm nine." "I wouldn't dream of it."); Big
              Sister's "Where have you come from?" (Awa, a writing school); and "Where did it GO, exactly?" "Out by the
              floats. It's floating. A ladle floats. That's the only good thing." (edo.fusaMet.)
              (2) Little Sister wades in (a click in the shallows; she is in her wading clothes while her feet are in the
              water): "Boots are for WATER." "She's in. Up to the top of the boots, and not one inch over." "It has a
              PASSENGER." (edo.waded.)
              (3) She pulls at the ladle: "Let GO, octopus. It's not your spoon." Heita, from his tub: "A tako lets go of
              nothing. Except for a crab." (edo.crabClue.) Big Sister: "Tako. Octopus. One of my forty words. Of course it
              is." (Asked, Heita says the same: "A tako lets go of nothing. Except for a crab." then "Crab.")
              (4) Mom at the rocks: "A crab, he says. Stand back, girls." She reaches under, and holds it up: "Got him.
              I've caught worse in a bathtub." Big Sister: "Mother just put her hand under a rock. I'm writing it down."
              (edo.crab: the crab in Mom's pockets.) Mom hands it to Little Sister (her portrait).
              (5) The crab on the ladle: "Here, octopus. One crab. Swap?" "It let GO. I've got the ladle." "And the crab got
              away. I watched it go. It's fine." Heita gets up, wades out to her and takes the octopus: "And the tako comes
              to me. Supper." He holds it up, goes back to his tub, and sits; she walks out of the water with the ladle
              (edo.ladleFree).
              (6) The ladle back (any of the three: Little Sister's "Here. Your ladle. It's got a bit of SEA in it.", or
              Mom's, or Big Sister's): "My LADLE. I don't care about the sea. It's mine." "You're going west? Then leave
              this at the women's hall at Shosha." "It's my name slip. My grandmother went there once. Don't lose it." "I
              won't. And here. A penny, for luck. It's got a man on it." "...He looks hungry." "Everybody says that."
              (edo.ladleBack: the slip to Little Sister, two pennies become one.)
Gives:        `edo.ladle`; the road west: Mom: "West, girls. One more day of road." and the card.
News:         O-Sato and her sister-in-law, Himeji women slipping away east to Ise (Mom or Big Sister, any time): "Then
              you'll know Shosha. We heard there's a voice there." "Still shut, when we left. And the voice still comes,
              every sunset." "Old O-Ume keeps it. She leaves the voice a rice ball, every evening." "Her husband made that
              lock. A shipwright, from Takasago." "And all he ever told her was that it opens to what a ship gives its
              lady." "Every woman in Harima has tried her comb in it. Mine twice." Big Sister: "...What a ship gives its
              lady. Hold on. I wrote something down on the ship." (edo.riddle: a help, not a gate; O-Ume gives the riddle at
              #37 too.)
Notes:        The octopus is drawn by the scene (a small pixel figure in the ladle's bowl, on the floor plane at the
              painter's [461, 430]) while the ladle floats; Heita holds it up as his supper. The shallows are ENGINE-21's
              `zones` on a floor that is the painter's sand and shallows joined: Little Sister's alone, the others refused
              with their own lines. The slip goes to Little Sister whoever gives the ladle back (it is hers to carry to
              O-Ume, and the penny is hers to give).
```

```
Card: The next day        (edo.walk2)
```
After "West, girls. One more day of road.": the card "The next day" / "Himeji", the portraits walking the act's map from
Akashi to Himeji (`g.journey("edo", "akashi", "himeji", { sound: "sandals" })`), and Himeji town at `east`
(`edo.inHimeji`). Skipped, the same place. Arriving: Little Sister: "There's the CASTLE. The white one, all the way up."
Big Sister: "And somewhere near here, a hall with a voice in it. At sunset." Mom: "Then we need the way there before the
sun goes. First things first, girls."

```
Puzzle #36: Supper For A Voice        (Act Six · Leads: each her own part · Himeji town)
Needs:        the card (edo.inHimeji)
Setup:        Midday in Watamachi. O-Kiku, seven, outside the writing school in her best clothes, not going in; her mother
              O-Tane at her door; O-Shizu teaching inside; Tōbei the night man at his hut, selling sandals and sweets by
              day; a komusō playing in the street. Three things want doing, one for each of them, in any order.
Wrong tries:  The lane north (the castle)       -> Mom: "Tomorrow. Tonight we go and listen." Big Sister: "The castle's
                                                   tomorrow. Jinsuke's lady can wait one more night." Little Sister: "Not the
                                                   castle YET. The voice first." (Mom, with supper made: "Shosha first,
                                                   girls. The sun won't wait, and neither will he.")
              The cotton office (Big Sister)    -> "They sell it in Edo, right over Osaka's head. Somebody's very clever."
                                                   Mom: "A matter of record: Gonroku's sail was a Harima captain's idea.
                                                   Woven cotton." "...You got that from the bosun." "I did. I listen to
                                                   bosuns."
              The well (Little Sister)          -> "Is it a WISHING well?" Mom: "It's a well well."
              The map, before supper            -> "Not yet. We don't go to a hungry boy empty-handed."
              The kitchen out of order          -> "Rice on dry hands. It's all over me. Water, then salt, then rice." (each
                                                   step early has its own line; nothing is spoilt); the plum before the rice:
                                                   "A plum goes inside a rice ball. First, a rice ball."
              The girls in the kitchen          -> "It's Mom's kitchen for the hour. I'm only here to say it looks right." /
                                                   "Mommy's cooking. I'm GUARDING the cooking."
              Tōbei's sweets (Little Sister)    -> "For sale. For children. For you, for the walk." "I'm saving it for the
                                                   walk. ...I ate it."
Solution:     (1) First day (Little Sister). "Is it your first day? Mine had a HAMSTER." "It bit the teacher. She was fine.
              First days get better." Then: "Come on. Together. I'll hold your hand. I'm good at hands." The two of them
              hand in hand along to the step stone and up onto the school's floor, their hats off indoors, to the two free
              desks. O-Shizu: "Two new girls. Good. Sit, both of you." "One character for you, small one. This is
              'mother'." "It's a mother with two eyes, looking at TWO children." "...That is not what the book says. It is
              better." Down again, hand in hand, to O-Tane at her door; Little Sister writes it in the dust: "Look. I can
              write one. It's 'mother'. Kiku, look." O-Kiku, smiling: "...Mother." O-Tane: "...That's the first word out of
              her all day." O-Kiku goes back in to her desk by herself (edo.kikuIn).
              (2) The way (Big Sister). "Your small sister brought O-Kiku in. Thank you." "She does that. She goes first."
              "Do you know the women's hall at Shosha? Could you tell us the way?" "My mother left her slip there every
              spring. Old O-Ume keeps it." "North-west, through the fields. The wooded mountain. The east path." "The hall is
              at its foot. An hour and a half's walk." "Go now, and you will be there before the sun is low." Big Sister:
              "She drew it. Pictures, no words. She drew it for somebody who can't read." (edo.knowWay: Shosha on the map.)
              (3) Supper (Mom). "May I ask a favor? We've a long walk tonight, and I'd like to take supper." "Supper. For
              the walk?" "For the walk. And one for a voice, in case." "...My kitchen's yours for an hour. The rice is
              cooked. Salt's in the jar." "Pickle's in the tub. And don't let the fire out." She holds out her paddle and
              Mom takes it; Big Sister: "Her paddle. Mom's been handed the keys to two kitchens this week."
              (edo.kitchenLent.) In the kitchen, in order: the bucket (or the well): "Water first. Wet hands, or the rice
              will cling to me like a toddler." "If that's my boy, he hasn't eaten. He never eats when he's worried."; the
              salt jar: "A pinch of salt, rubbed into wet hands. Now the rice."; the rice pot: "A handful, and press.
              Bale-shaped, the way they do here. And again." (Big Sister: "Bale-shaped: the Kansai way. Edo does triangles,
              mostly. You're doing it right."); the plum jar, if she likes: "A plum in each, for the road."; the pickle
              tub: "A slice of pickle beside each one. Now the cloth."; the cloth: "Wrapped. One each for the walk, one for
              the keeper, and one for the voice." "...In case." (edo.riceballs: the rice balls in Mom's pockets.)
Gives:        `edo.supper` (edo.supperMade as they leave for Shosha by the map): "Shosha. An hour and a half's walk,
              north-west."
Notes:        O-Kiku and Little Sister walk hand in hand (`edo-hand`, `kiku-hand`) and climb to the school's floor by
              `g.climbTo` from the step stone; the school is a floor of its own at the painter's scale. The kitchen's order
              is a small puzzle of its own; out of order is a funny line, never a failure. The plum is optional.
```

```
Puzzle #37: What A Ship Gives Its Lady        (Act Six · Leads: all three at once · the foot of Mount Shosha)
Needs:        supper (edo.supperMade)
Setup:        Late afternoon. The women on the bench, waiting with their slips: Grandmother Tome: "It's a fox, I tell you.
              Foxes like a sunset." A wife: "A fox wouldn't call every evening at suppertime." O-Ume: "A boy who calls at
              suppertime is a hungry boy." The hall shut, the lock on its hasp, a rice ball on a leaf on the step, Ryōkai
              sitting by the stone at the foot of the path.
Wrong tries:  The path up (the first try)       -> Ryōkai on his feet: "Forgive me. Women may not climb." "Not since long
                                                   before my grandmother's grandmother." Mom, her own first try, prays:
                                                   "'Hear my cry, O God; attend unto my prayer." "From the end of the earth
                                                   will I cry unto thee, when my heart is overwhelmed:" "lead me to the rock
                                                   that is higher than I.'" Big Sister: "Psalm 61." Mom: "He'll have to come
                                                   down to me, then. I'm not allowed up." Big Sister: "We're not allowed up,
                                                   so I'm going to be very interested in the bottom." Little Sister: "I'm only
                                                   SEVEN." Ryōkai: "Girls are women, for this."
              The rice ball on the step         -> Little Sister: "That's HIS." "It's his supper. I'm not even LOOKING at it."
              The bench                         -> Little Sister: "I sat on the END. A grandma moved over. Nicely."
              The road back (east)              -> "Not now, darling. The sun's going down. That's the point of being here."
              The pin and the coin in the       -> "A pin won't turn a square post. It wants a square hole." / "The pin's busy
              wrong places                         in the EAR." (each part has its wrong things, each with its line)
              One person at two parts           -> "I've got two hands, and one of them is in a rabbit."
              The wrong hand at a part          -> Big Sister at the ear: "The ear-pick end fits the hole. Forty years of
                                                   dust, out." "...My fingers are too big for a rabbit." Mom: "I can't push it
                                                   home. My fingers are a civilized size." Little Sister at the post: "It fits.
                                                   It won't TURN. Not with my other hand." Mom at the slits: "My hands are
                                                   shaking. Somebody steadier."
              Step back with it held            -> everything springs back: "And everything springs back. Patient thing,
                                                   isn't it." / "It all sprang back. Forty years of waiting. It can wait one
                                                   more minute." / "It all went BACK. The bunny's sulking."
The talk:     Ryōkai (optional): what is up there that they will not see (the founder's hall and its strongmen, the bell,
              and "A stone with a great lady's poem on it. Very old." "She asks the moon at the mountain's edge to light her
              road, from far off." Mom: "...I know that one. Not the words. The asking."). O-Ume: the voice, the abbot's
              word, and the riddle: "It opens to what a ship gives its lady. That's all he ever said." "He liked a riddle
              better than his supper." The slips from Osaka and Akashi into her hands: "Then I'll hold it till the door
              opens. It will open. Doors do." (edo.oumeMet; edo.natsuGiven, edo.fusaGiven.)
Solution:     (1) The lock up close (the lock, from any of them): the first time, Tome: "Thirty times. My best comb. It
              looked at me." (edo.lockSeen.)
              (2) Big Sister's note on the rabbit (the riddle known): "Here. What the shipwright seals in the mast, for the
              lady." "Two dolls. Two dice. Twelve one-mon coins. A woman's hair. The five grains." "And?" "Rouge. Powder. A
              comb. A pin." "Every woman in Harima tried her comb and her pin. Nobody tried a coin." Little Sister: "I've got
              a COIN. With a hole in it. From Kōta." Mom: "And I have a comb from Osaka. And you have a pin in your hair,
              darling." (edo.listRead.)
              (3) The hand-round, by the portraits (each its own line, and once Little Sister's "Everybody give your thing
              to the NEXT person. It's like a party game."): the pin to Little Sister ("Small fingers. Mind it, it's
              O-Tami's."), the coin to Mom ("It's Kōta's coin, Mommy. Turn it NICELY."), the comb to Big Sister ("Steady
              hands, darling. It's O-Natsu's comb.").
              (4) The ear: Little Sister's pin: "In it goes. Click. The wave MOVED. I'm holding it." (edo.earHeld; her hand
              drawn holding it.) (5) The post, under the wave: Mom's coin: "It fits the post. A quarter turn. Stiff.
              ...Click." "Something opened along its back. I'm holding." (edo.postHeld; her hand drawn, turned.) (6) The
              slits: Big Sister's comb: "Teeth into the slits. Steady. ...Press." "The springs closed. I felt them. The
              bolt's free." "It CHIRPED." "Like the ship. Exactly like the ship." O-Ume: "That's him. That's his joke. The
              lady chirps."
              (7) Back outside, the sun going red: the doors swing open (edo.hallOpen). O-Ume: "In you go. Slips first.
              Grandmother Tome, you've earned the front." "These two go up first. They came farthest." Mom: "And this is for
              you. From a kitchen in Watamachi." "...I've left out thirteen of these. Nobody ever left me one." Little
              Sister: "And this. It's from a boy on a ship. For your rice balls." "...From a ship." "Then it's come home."
              The comb back to Mom, the pin back to Big Sister; the women go in with their slips and come out and go home
              ("In, and out, and home before dark. Thank you." "Grandmother's slip is in. I'm running home. All the way.");
              O-Ume takes the rice ball from the step and goes in; Ryōkai goes round to the lattice. Mom: "The sun's going,
              girls. Inside."
Gives:        `edo.hall`; the hall's doors.
Notes:        The three hands are ENGINE-21's `g.hand` with PEOPLE-21B's `LOCK_HANDS` (Mom's with `coin: false`: the coin is
              painted on the post); the held facts are momentary (never saved: a load finds the lock shut, and Step back
              lets everything go). The hidden post's own look and use are never reached (the middle wave covers it until
              the ear is held). The sunset is the painter's sunset layer and the cut-outs' `-sunset` twins, faded in as
              the doors open (`g.fadePlane`).
```

```
Puzzle #38: A Small Door At Sunset        (Act Six · Leads: Mom, then all · inside the women's hall)
Needs:        the hall open (edo.hallOpen)
Setup:        Inside. O-Ume: "Sit where you like. He comes when the light reaches the wall." Grandmother Tome, at the
              hum, goes home: "Thirty-one tries, and now I go home to my supper. Goodnight, all." (edo.tomeHome.) Bars of
              red light lie low on the east wall and climb, slowly, while they look round.
Wrong tries:  The cabinet                       -> O-Ume: "Kannon-sama is in there. You don't open her." Big Sister: "The one
                                                   who hears the cries of the world. That's what the name means." O-Ume: "So
                                                   she does." Mom: "So does mine."
              The flashlight, before the sun    -> "Not yet. The SUN has to find it first. Then my light."
              The rice ball into a coin         -> "It won't fit. Not through a coin."
Solution:     (1) The voice: when the bars reach the hum, the small door opens, the size of a coin, and Mom is the one
              played: "Hello? It's me again. Day fourteen." "Is anybody there? Anybody? ...Even you, Closet?" Mom: "It's not
              a closet. It's a temple." "...MOM?" She kneels by the wall (edo.sonHeard). "You went through. I TOLD you not
              to." "You did. You were right, and we went anyway, and we're all right." Little Sister: "Is that YOU?" "Is
              that YOU?" "I asked EARLIER."
              (2) The talk (Mom first; the girls each their own, by the door): where they are, his fortnight, where he
              sleeps; Big Sister's walnut and her theory ("Mother. I have a theory. I can't footnote it.", after Little
              Sister's penny); Little Sister's penny, the chickens, and whether he is scared; and Mom's "Have you eaten?"
              "...Define eaten." Little Sister: "MOMMY. The rice balls." (edo.eatenAsked.)
              (3) More light, more door: Little Sister's pink flashlight on the door: "More light, more DOOR." "Whoa. The
              door got bigger. And PINK." (edo.doorWide: the size of a hand.)
              (4) Supper: the rice ball into the door (`g.send("riceball", { to: "son" })`): "Here, darling. Supper."
              "It's cold. It's rice. It's the best thing I've ever eaten." "Chew." "I AM chewing." O-Ume, laughing and crying:
              "I don't know a word of it. I know eating." (edo.sonFed.)
              (5) Tomorrow: "Tomorrow there's a door at the top of a castle. We're bringing your coin." "..." "Mom. Dad went
              through alone." "Don't. Whatever happens, hold hands." "We will." (edo.holdHands.)
              (6) The sun goes: "Mom? The sun's going. The keys are going dark." The bars fade, the pink light with them:
              "'Can a woman forget her sucking child," "that she should not have compassion on the son of her womb?" "yea,
              they may forget, yet will I not forget thee.'" Big Sister: "Isaiah 49:15." The door shrinks and is gone, and
              the hall is dusk. O-Ume: "Will he come again tomorrow?" Mom: "I think so. If he does, feed him."
Gives:        `edo.son`; the cut-scene.
Notes:        The bars are the scene's own live layer (blended light, moved by the light's k: low at 0, the hum lit at
              0.563, a coin's door at 0.6, a hand's at 0.68, the sunset 0.78), the door ENGINE-21's portal at the painter's
              [652, 316] (a coin's r 9, a hand's 19). Nobody stands in front of the hum: the wall's things are looked at
              from a step back (`big`, `mid`). The Son's talk is played plainly (`g.talk(sonTree(h))`); his lines through
              `sonVoice`. The rice ball waits in the tunnel for him (the engine's letterbox keeps it). The mirror stays in
              Mom's sleeve.
```

```
Cut-Scene: Mind The Fire        (edo.night)
```
The title: "Mind The Fire". At the hall's step in the dusk, O-Ume with a paper lantern: "Take the lantern. The fields are
dark, and the frogs are loud." "Thank you, O-Ume." "Keep it till you're done with it. A lantern is a patient thing." The
dark fields, the frogs, the family a small group of shapes with the lantern on the path, the castle a pale shape on its
hill: "The frogs are SINGING. All of them. Not well." "The castle. Just a pale shape, up there in the dark." "One more
night, darling. Then the castle." Himeji by night, the ward gate shut, Tōbei with his clappers: "Hi no yōjin. Hi no
yōjin!" "...Late walkers. With O-Ume's lantern. From Shosha, then." "The gates are shut. That's what a gate is for, at
night." He strikes his signal, and the gate opens: "There. The next man will let you through, and the next. Gate to gate."
Big Sister: "We're being POSTED." Little Sister: "Arigatō, clapper man." "Mind the fire." O-Tane's door, a crack of light:
"In. Quietly. She's asleep, and she's had a day." "So have we. Thank you." The dark: "He ATE it." "He did." "Tomorrow we
hold hands." The card "The next day", and the castle approach at `enter` (`edo.nightDone`), the three in O-Tami's clothes,
hats on. Skipped, the same place and clothes.

```
#39 to #41 and Hold Hands        (round twenty's #28 to #30: as built)
```
The castle approach is reached the morning after "Mind The Fire" (`LEG_START.himeji` holds `edo.nightDone`; #39 needs
`edo.night`). New at the castle: the road back into the town at the left edge (to its ward gate; the lane north brings
them up again), and the map, which refuses Shosha: "Shosha's done its part. Today it's the castle." In Hold Hands, Little
Sister's new line comes first, before Mom's "Places, girls. Hold hands. All the way through.": "My brother SAID."

### Ledger rows

**Things that are carried** (the stretch's part)

| Thing | Comes from | Who can hold it | Used for |
| --- | --- | --- | --- |
| O-Fusa's ladle (`ladle`) | The Akashi shore (#35): freed from the octopus | Little Sister (any of them, handed round) | Given back to O-Fusa: her slip and Little Sister's penny |
| A crab (`crab`) | Under the rocks (#35), Mom's | Mom; then Little Sister | Swapped for the ladle: the octopus lets go (the crab gets away) |
| O-Fusa's slip (`fusaslip`) | O-Fusa (#35) | Little Sister | Into O-Ume's hands at Shosha (#37), and up first in the hall ("They came farthest.") |
| Little Sister's pennies (`twopennies` -> `lastpenny`) | Act Six, as built | Little Sister | One for O-Fusa's luck ("He looks hungry."); the last stays |
| The rice balls (`riceball`) | O-Tane's kitchen (#36), Mom's making | Mom | One for O-Ume (#37), one through the door for the Son (#38) |
| O-Natsu's slip (`natsuslip`) | Osaka (#29) | Mom | Into O-Ume's hands (#37) |
| O-Tami's hairpin (`kanzashi`) | Big Sister's (#22) | to Little Sister for the lock, and back | #37: the ear (cleaned, and held) |
| Kōta's one-mon coin (`mon`) | Little Sister's (#27) | to Mom for the lock, and back to Little Sister | #37: the post (turned, and held); then given to O-Ume ("Then it's come home.") |
| O-Natsu's comb (`comb`) | Mom's (#29) | to Big Sister for the lock, and back | #37: the slits |
| Big Sister's note (`note`) | the Funadama's list, from the ship (#27) | Big Sister | #37: read against the riddle (a comb, a pin, a coin) |
| Little Sister's pink flashlight (`lilflash`) | Act Three | Little Sister | #38: more light, more door (and #40, as built) |

**Clothes**

| Who | From | To |
| --- | --- | --- |
| Little Sister | `edo` on the sand | `edo-wading` while her feet are in the shallows (#35); `edo` again on the sand |
| Little Sister (and O-Kiku) | `edo` | `edo-hand` (and `kiku-hand`) hand in hand to the school and back; `edo-hatback-hand` on the school's floor, `edo-hatback` at the desk (#36) |
| all three | `edo` outdoors | `edo-hatback` (hats on their backs) inside the women's hall (#38); `edo` again for the night and the castle |

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| The Funadama's list (Big Sister's note: a comb, a pin, twelve one-mon coins) and the lady's chirp | #27, on the ship | #37: "What a ship gives its lady"; the lock chirps ("Like the ship. Exactly like the ship.") |
| Kōta's one-mon coin with its hole | #27 | #37: the square post; given to O-Ume ("From a ship." "Then it's come home.") |
| O-Natsu's comb, O-Tami's hairpin | #29, #22 | #37: the slits, the ear |
| The slips (O-Natsu's from Osaka, O-Fusa's from Akashi) | #29, #35 | #37: into O-Ume's hands; up first in the hall |
| "If that's my boy, he hasn't eaten." Mom's Nevada "Have you eaten?" | #36, the well; Nevada | #38: "...Define eaten."; the rice ball through the door |
| More light, more door (the keep's rule, Act Four's sun shade) | #38, the pink flashlight | #41: the mirror, backed away |
| "Whatever happens, hold hands." | #38, the Son | Hold Hands: "My brother SAID." |
| Tōbei, the night man, and his clappers | #36, his hut by day | Mind The Fire: gate to gate |

## Act Six, the castle at Himeji (#39 to #41; round twenty's #28 to #30), and "Hold Hands", as round twenty built them

<!-- MERGE-21: renumbered in play order; the castle is reached the morning after "Mind The Fire" now: see the road west part above. -->

The third of the act's three legs, as built in round twenty: the castle at Himeji in the spring of 1830, three days after
the hills, and the end of the demo. MERGE-20 joins this part with SCENES-20A's (Yui) and SCENES-20B's (the hills) into
`docs/PUZZLES-japan.md`. The lines are WRITE-20B's (`js/content/lines/edo-b.en.js`), quoted here as the game says them, in
the order it says them; the talks are WRITE-20B's trees (`js/content/talk/edo-b.js`), staged by the scenes
(`js/content/scenes/edo-castle.js`, `edo-keep.js`, `edo-keeptop.js`, and what they share, `edo-himeji.js`) and the
cut-scene (`js/content/cutscenes/edo-step.js`).

### Puzzle structure

```
          (from the hills: "Three days later", the road into Himeji: edo-walk, SCENES-20B's)
                                        |
         #39 Eight At The Gate (all three; the castle approach)
             Little Sister hollers Tomezo down his ladder; Mom gives back his trowel with Jinsuke's
             news; three hands short, three here: the head-cloths, a bucket each; the count
             -> eight went out, eight come in (edo.inside): the keep
                                        |
         #40 A Light That Needs No Fire (Little Sister; inside the keep)
             the warden at the stairs, his poems, the lady of the keep, no fire in a wooden keep;
             the pink flashlight shown, and lent: the lime may come up to carry it (edo.up)
             -> the climb, floor by floor, in the dark: "Two." ... "Six."
                                        |
         #41 The Lady Of The Keep (Mom; the top floor, at sunset)
             the truth, first; the west window (the bar is the warden's); the mirror on the hum:
             a letterbox; Mom backs into the window, step by step: a doorway, the cross in it;
             the coin into Mom's hand; the mirror to the warden, for Tomezo (edo.door)
                                        |
         Cut-scene: Hold Hands  ->  card: "to be continued"  ->  the title (edo.done, demo.done)
```

Goal of the leg: **get to the top of the keep, where the hum is, and through the door.** The leg begins at
`LEG_START.himeji` (`js/content/scenes/edo-common.js`): the castle approach at `enter`, the three of them in O-Tami's
travel clothes with their hats on, Mom carrying the grandmother's bronze mirror and Jinsuke's trowel, Big Sister the coin,
Little Sister her pink flashlight.

The beats (`js/content/acts/edo.js`), each with the fact it makes true: `edo.inside` (#39: it needs `edo.walked`), `edo.up`
(#40), `edo.door` (#41) and the gate `edo.end` (Hold Hands, `edo.done`; with it the demo's end, `demo.done`). Each puzzle's
hint follows how far it has got, for each of the three (the facts the scenes set for it):

| Puzzle | Stage | The fact that moves it on | Mom's hint at that stage |
| --- | --- | --- | --- |
| #39 | Tomezo up his ladder | `edo.tomezoDown` | "The man in white up the ladder is Jinsuke's cousin. Your sister can reach him." |
| #39 | the trowel still carried | `edo.trowelBack` | "His own trowel back in his hand, and Jinsuke's name. He'll understand the rest." |
| #39 | not yet crew | `edo.crew` | "He's three hands short and we're three. Head-cloths and buckets, and we're crew." (never at rest: see #39's notes) |
| #39 | crew, at the gate | `edo.inside` | "Eight went out, eight go in. Carry lime, say nothing untrue. The count holds." |
| #40 | the warden not met | `edo.shinMet` | "The young man at the stairs fears the dark. Your sister has what he needs." |
| #40 | the light not shown | `edo.lightShown` | "He may carry no fire up. Your sister's flashlight isn't fire. Let her show him." |
| #40 | the light not lent | `edo.up` | "Lend him the light and we go up to carry it. That's a reason the lime may climb." |
| #41 | the truth not told | `edo.truth` | "He thinks I'm the lady. The lady asks for the truth. I'll give him mine first." |
| #41 | the west window shut | `edo.window` | "The west shutters are barred, and the bar is the warden's. Ask him." |
| #41 | the mirror not in the beam | `edo.letterbox` | "Sun behind me, the mirror in my hands, its light on the hum. Light opens them." |
| #41 | the letterbox, Mom not at the window | `edo.doorway` | "More light, more door. The farther I stand from the wall, the bigger the patch." |
| #41 | the doorway, the coin not in Mom's hand | `edo.door` | "The coin steers. Whoever has your brother's coin, I'd like it in my hand first." |

### Location layout

Three places, one painting each, all at Himeji in the late afternoon and the sunset, one place on the act's map (`himeji`,
the third leg: no travel within it). The castle approach leads in through the gate only by the count; the keep's ground
floor leads up only by the warden's stairs; there is no way back down (the act ends at the top).

```
THE CASTLE APPROACH (edo-castle): late afternoon
+------------------------------------------------------------------------------------+
| the SKY                         the KEEP, white, roof on roof,                      |
|                                 on its STONE BASE             the HILLS            |
| the double CHERRY,                                     the GATE tower: on its GABLE |
| in full late bloom      the WHITE WALL, the SCAFFOLD    a round tile with a cross;  |
| (its petals falling)    with two men on its lifts;      TOMEZO up his LADDER;       |
|                         the TUB of lime, its mixer;     the two GUARDS in the       |
|   the MOAT, still, the  the three BUCKETS               opening                     |
|   HERONS and egrets all     the TERRACE  /  the stone RAMP up to the gate           |
|   facing the keep                                                                    |
|   the ROAD below: PILGRIMS with ladles, going east (now and then)       Here: enter |
+------------------------------------------------------------------------------------+

INSIDE THE KEEP (edo-keep): the ground floor, dim
+------------------------------------------------------------------------------------+
| the CEILING, beams                                                                  |
| the STAIRS, steep    the great PILLAR   the GUN PORTS: round, triangle, square      |
| as a ladder,                            (each throws a BEAM of sun of its shape     |
| up through the                          across the floor)        the WEAPON RACKS   |
| ceiling                                     the STONE-DROP window  (spears, guns:   |
|   SHINNOSUKE at their foot                                          scenery)        |
|                     the FLOOR, dark boards     the CREW: Tomezo, one mixing, one    |
|   the plank, brushes                           trowelling the wall   the TUBS       |
|                                                               Here: enter (doorway) |
+------------------------------------------------------------------------------------+

THE TOP OF THE KEEP (edo-keeptop): the top floor, sunset
+------------------------------------------------------------------------------------+
|                         the RAFTERS, going up into the dark                         |
| the WEST shutters   the NORTH shutters (chests below them)     the EAST shutters,  |
| (open: the WINDOW,  the old LANTERN                            and before them the  |
| the VIEW of the town                                           HUM, a shimmer: the  |
| and the Inland Sea,                                            DOOR, in the light   |
| the HERONS going by)        the FLOOR (dust; the sun's beam across it when open)    |
| the rail round the stairwell     SHINNOSUKE at the top of the stairs   Here: stairs |
| (the SOUTH shutters: behind us)                                                     |
+------------------------------------------------------------------------------------+
```

### Cut-scenes and puzzles

```
Puzzle #39: Eight At The Gate        (Act Six · Lead: all three · the castle approach)
Needs:        the walk into Himeji (edo.walked)
Setup:        The gate counts everyone in and out. Tomezo the plasterer, Jinsuke's cousin, is up his ladder against the
              gate tower shouting at nobody: "Three of you, gone to Ise with ladles, and the lime going off in the tubs!"
              "Kichi. Yasu. Whoever the third one is. Come back and I'll only shout a LITTLE." His crew of four at work:
              two on the scaffold's lifts trowelling the wall, one at the tub with the mixing pole, one behind the
              scaffold. Pilgrims pass on the road below now and then, ladles held up ("To Ise! To Ise, before the master
              notices."). The herons in the moat all face the top of the keep.
Wrong tries:  The gate                          -> Mom: "They asked my name, my house and my business. I have one of the
                                                   three." Big Sister: "I can't walk through a gate that counts. Not
                                                   without a number of my own." Little Sister: "I tried to walk in SMALL.
                                                   They counted me anyway. ...They count small."
              The guards (asked by Mom)         -> "Name." "House." "Business." Mom: "I'm a traveller, and I'd rather not say
                                                   the rest. That's true, and all of it." "A traveller with no house and no
                                                   business does not come through this gate." "She may stand on the ramp.
                                                   The ramp is free." (and "I'd like to see the keep. From inside." "So
                                                   would the town." "The town looks from the moat. With the herons.") Mom
                                                   will not lie, so she cannot answer: "Then we'll leave you to your
                                                   counting." "Three, out. Though you were never in."
              The guards (Big Sister)           -> "What are you counting?" "Everyone." "In. Out. The number must be the same
                                                   by sundown." "...And if it isn't?" "It is always the same. We count."
                                                   (the clue: eight)
              The guards (Little Sister)        -> "Why do you have TWO swords each? One's plenty." "One is for wearing."
                                                   "The other is also for wearing." "...That's a good answer. I'm going to
                                                   use that." And the tile: "We know." "Nobody knows who put it there. We
                                                   count people. Not tiles."
              Tomezo, asked politely (Mom)      -> "Excuse me. Sir. ...Excuse me." "And the gate wants eight back by sundown,
                                                   and I've got FIVE--" "He can't hear courtesy from down here. It doesn't
                                                   carry." (and the trowel held up to him: he does not see it)
              Tomezo, waited out (Big Sister)   -> "We could wait till he runs out of breath." "--and the lord's steward
                                                   coming Thursday, and who's he going to shout at? ME." "He isn't going to
                                                   run out. He's got a system."
Solution:     Little Sister cups her hands round her mouth: "Hey. Mister Plaster. DOWN here." "...Who said that?" "Me. I'm
              small. Look DOWN." "...A child. In yellow boots. Hollering at a man up a ladder. I'm coming down." He climbs
              down the ladder, turns to her: "You're not from here. None of you. What do you want with a plasterer?"
              (edo.tomezoDown.) Mom holds out his trowel: "I believe this is yours. Jinsuke sends it back, and says he's
              well." It goes into his hand; "My trowel. Where did you... You've seen Jinsuke?" "...He's well?" "He's well.
              So are his mother and his daughter." "..." "Right. ...Right. I'm not asking you one thing more, and you're
              not telling me." Big Sister: "That's how we know he knows." (edo.trowelBack.) "Three short, and three
              standing in front of me. I don't argue with arithmetic." "Head-cloths, white, like mine. Bucket each. Carry
              it from the bottom, tall one." The three of them in the plasterers' white head-cloths, one after another.
              "I'm a plasterer now. I'm a PLASTERER." "You're a bucket. Everybody starts as a bucket." (edo.crew.) The
              gate, or the guards, now: Tomezo to the gate; the two lifts come down, the crew gather; the three take up a
              bucket each ("Tall one. Bucket from the bottom. ...Like that. Now you're a plasterer."). "Plasterers. Eight
              out this morning. Eight back. With lime." The crew go in, Tomezo last of them: "One. Two. Three. Four.
              Five." Mom and Big Sister up the ramp with their buckets: "Six. Seven." Little Sister last, at the
              threshold: "...Eight." "Eight went out. Eight come in. The number is right." "We are eight. We are carrying
              lime. All true." "The small one is also carrying lime." "With BOTH hands." "...Eight. Through." Through the
              gate, and into the keep (edo.inside).
Gives:        `edo.inside`: the keep's ground floor, with the crew.
The cross:    From the ramp, the gable over the gate: the first time Big Sister looks, "A cross. On a castle gate. Nobody
              knows who put it there." Mom: "Somebody did." (After that, each her own look at it.)
The cherry:   Little Sister lies down under it (`edo-lying`): "I'm lying under it. The petals land on my face. ...One went
              up my NOSE." Big Sister shakes a branch: "It snowed pink. I'm not sorry."
Notes:        Staged in the scene (the tree's lines in the tree's order; ready.md lists each): the trowel changes hands as
              Mom offers it, before his lines; the head-cloths go on after his "Head-cloths, white, like mine", before
              Little Sister's "I'm a plasterer now"; the count is said while the eight walk through. The tree goes from the
              trowel straight on to the head-cloths, so the hint's third stage ("not yet crew") is never asked at rest.
              Before the crew, everyone in Tomezo's talk down below has the way out (Mom's "Then we'll carry lime, and say
              nothing untrue."); Little Sister's is her own ("Arigato, Mister Plaster." "...See? Can't manage it.").
```

```
Puzzle #40: A Light That Needs No Fire        (Act Six · Lead: Little Sister · inside the keep)
Needs:        the count (edo.inside)
Setup:        The crew at work at the right, their backs to the stairs on purpose; the first time in, the bucket goes to
              the tubs ("Bucket here, tall one. Mind the floor. The floor's older than the lord.") and the three walk a few
              paces in. At the foot of the stairs, Shinnosuke, the warden's son, nineteen, holding on to them, making
              poems: tonight he keeps the top floor alone, on a dare, with the lady of the keep. No fire may go up a wooden
              keep, so he goes up into the dark.
Wrong tries:  The stairs (he is at them)        -> "No one goes up. Except me. Tonight. Alone. With the lady." Mom: "He's
                                                   quite right, and he's quite frightened. We'll talk to him first."
              The weapon racks                  -> Mom: "No."
              The gun ports                     -> the shapes (Big Sister); Little Sister tries the triangle with one eye
              The great pillar                  -> Little Sister hugs it ("one tree, all the way up")
              Mom's offer, before the light     -> "We could come up with you. Three more people is three fewer darks."
                                                   "Three more people in the dark is three more people in the dark. Thank
                                                   you. No." "If one of you had a light that was not fire, I would say yes
                                                   at once."
              Little Sister, asking to go up    -> "Can we come up with you? I'm good at dark." "No one goes up. Except me.
                                                   Tonight. Alone. With the lady." "You said that already. It's not a better
                                                   rule the second time."
The talk:     Meeting him: "You're the lime. Good. Lime is on the ground floor." "Everything is on the ground floor. Except
              me. Tonight." "You seem a little..." "I am making poems. It helps. It does not help." His poems, five, seven
              and five, one for each asking ("Sunset. Stairs. Dark. Me." / "Everyone I know is down." / "I am the top
              part."), Big Sister counting on her fingers each time ("Five. Seven. Five. ...He's doing it on purpose."); the
              lady of the keep ("She comes to anyone who climbs up in the night, and asks them why." "If they tell her the
              truth, she is kind. Everyone says so. Nobody has tested it." Mom: "Then tell her the truth, and she'll be
              kind. Those are all the instructions."); the dare (Big Sister: "Why are you going up at all?" "A dare."); no
              fire in the keep (Big Sister: "So it's the dark you're frightened of. Not the lady." "It is both. They are
              friends."); Big Sister's own poem ("...I've run out of five."), and Little Sister's chicken.
Solution:     Little Sister: "I've got a light with no fire in it. Look. Press the END." The pink light on his face:
              "...!" "It is cold. It is light, and it is cold. There is no fire in it. I have looked." "That is the most
              wonderful thing in Harima. It is pink." "Pink's the best colour of light. Everybody keeps SAYING it isn't."
              (edo.lightShown.) Then: "You can borrow it. For the lady. You have to give it BACK, though." "I could not. It
              is yours. It is the only one." Mom: "We'll carry it for you. We'll come up with you." "...The lime may come
              up. To carry the light. Nobody said the lime may not." Big Sister: "That's the fastest I've seen anyone
              change a rule. Four seconds." "I have stood here since noon with the words ready. Only the reason was
              missing." The light goes into his hands (he holds it in both, lit, like something holy). Mom: "Up, girls.
              Behind the gentleman with the light. Short steps." (edo.up.)
The climb:    Up the stairs, the warden first with the light, then Little Sister, Big Sister and Mom, out of sight through the
              ceiling; then the dark, a small pink light going up through it, a line a floor: "Two." (Big Sister) "Three.
              It's getting DARK." "Four. Hold the light up, small one. Higher. ...Thank you." "Five. The stairs are getting
              steeper. Or I'm getting older." And the top floor, Mom leading: "Six. The top, girls. A door at the top of
              the stairs, and a hum behind it."
Gives:        `edo.up`; the top floor, at sunset (`edo.climbed`, the scene's own).
Notes:        Staged: the flashlight comes on in his face before his "...!", not after his four lines about it. The stairs,
              once he has the light: "Up, girls..." and the climb, from any of the three.
```

```
Puzzle #41: The Lady Of The Keep        (Act Six · Lead: Mom · the top floor)
Needs:        the climb (edo.up)
Setup:        The top floor, the shutters closed, the last of the day coming through the cracks of the west ones; the
              hum in the east wall, heard low as they come up and growing, and, looked at long enough, seen: a shimmer in
              the air. Shinnosuke at the top of the stairs with the pink flashlight in both hands.
Arrival:      Mom: "Six. The top, girls. A door at the top of the stairs, and a hum behind it." She takes the grandmother's
              mirror out and holds it up to what light there is: in the half dark, a tall woman in a pale kimono with a
              mirror. He turns with the light, and falls to his knees: "...Lady." "I came up on a dare. I am telling you
              first, before you ask." "Because that is the story, and I am in it." "Are you the lady of the keep?" (The
              question hangs: the answer is Mom's to give.)
Wrong tries:  The girls, to him                 -> Big Sister: "She's our mother. For the record. Not a ghost. I've checked
                                                   for thirteen years." "A ghost would have a daughter say that." "...That's
                                                   actually a good point. Mom, you'd better tell him yourself." Little
                                                   Sister: "That's my MOMMY. Ladies of keeps don't have me. I'd know."
                                                   "...Does the lady of the keep have children?" "Ask her. She tells the
                                                   truth. It's her RULE."
              Mom's other answers               -> "Do I look like the lady of a keep?" "Yes." "...That's the trouble with
                                                   asking honest people questions." "Please stand up. Nobody kneels to me.
                                                   My children don't even sit when I ask." "I will stand. I will still have
                                                   asked." "You came up on a dare, and you said so before anyone asked you.
                                                   That was brave." "It was the story. In the story, the truth comes first.
                                                   I had no better plan." "There isn't one. We've tried."
              The west shutters                 -> barred: "The bar is the warden's to lift. I'll ask him. Properly."
              The other shutters                -> "It's not the window we need, darling." (south) "No. Not that one."
                                                   (north) "I'm not opening the east. The sun's gone from there. It's the
                                                   west we want." (Big Sister: "I'm not going to open every shutter in a
                                                   castle. The west one. Focus.")
              The mirror on the hum, in the dark -> "In the dark it's only bronze. It needs the sun behind me."
              The coin on the hum               -> "Not yet. The coin's for the walk through, not for the wall."
              The lantern                       -> "I'm not lighting anything in a wooden castle, darling."
Solution:     (1) The truth. Mom: "I'm not a lady of anything. I'm a mother looking for my son." "I think there's a door up
              here. I think it might go where he is." "...You did not have to tell me that. I had already knelt." "I know.
              That's why I told you." "Then the story is the other way round tonight. The lady is honest with the boy." He
              stands, the light in his hands again; Mom lowers the mirror (edo.truth). (2) The window. "Would you lift the
              bar on the west shutters? I need the sun. The bar is yours." "The bar is the warden's. ...I am the warden.
              Tonight." "Stand back from it, small one. It has not been lifted in my lifetime." He goes to the west bay and
              lifts the bar; the shutters swing open: "The SUN. It came in all at once." "Low and orange, straight across
              the floor to the east wall. That's our light." (edo.window.) (3) The mirror. Mom at the hum with the mirror
              held up in the sun: "Here. The sun on the face of it, and the light of it onto the hum." A hand-sized patch
              of light on the wall, and in it the shimmer flares into rings: a small door. "It opened! A little one. A
              LETTERBOX one." "The air through it smells of... not here. Dust and sun and something cooking." "Not big
              enough. Not nearly." Big Sister: "These mirrors are a little convex. The face bulges, barely. The light
              spreads." "The farther away you stand, the bigger the light. More light, more door." "Back up, Mom. Keep
              going." (edo.letterbox.) The player backs Mom away from the wall across the floor, step by step (the floor is
              "Back away across" while she holds the light; the west window takes her all the way), the patch and the door
              growing at every step, the size of a plate ("A plate. A lid. A door. Keep GOING, Mommy."), of a door, into
              the very mouth of the west window: "I'm in the window. There's no farther. ...Oh. Oh, look at it." "A
              doorway. The rings go right out to the edge, and in the middle..." "There's a CROSS in the door." "...A
              light nobody lit. At the top of the keep." "Every child in Harima knows it, and I am looking at it." "You lit
              it, in a way. You lifted the bar." (edo.doorway.) (4) The coin. If Mom has it, at once; if not: "The coin
              steers. Whoever has your brother's coin, I'd like it in my hand first." and whoever has it gives it to her
              (handed over, or asked for: a word between them): "The coin, Mom. If it listens to anything, it'll listen
              to that." (or Little Sister: "Here's the coin, Mommy. It's been where we're going. Maybe it remembers the
              WAY.") "I have it. Your brother's coin, in my hand. Then we steer by it, and we hope." "This is for Tomezo the
              plasterer. He'll know whose it is, and where it goes." "A warden does not take things from the lady of the
              keep." "I'm not the lady of the keep. I'm a mother, asking you to carry a mirror down." "...Then I will
              carry it. Carefully. In both hands. I have had practice tonight." He comes to her in the window, and the
              mirror goes into his hands, its light with it: he keeps it on the hum while she steps out of the window's
              mouth and he steps into it (edo.door).
Gives:        `edo.door`; the cut-scene.
Notes:        The light is the engine's `mirror` kind driving a `portal` (the door), at the painter's numbers: the patch 27
              cm across with Mom at the hum, two metres at the window (D = 12 + 0.254 d), squeezed as the wall is seen. The
              tree is played in three goes (ready.md): the letterbox; the player backs Mom away; the doorway, and the coin
              (handed to her, or asked for) if she has it not. While Mom holds the light she stays where she is: the floor
              is where she backs to. The door itself, touched: the hint's line for where she is. The flashlight on the
              hum and the other shutters opened are there for a script only (the light is lent before the top floor; only
              the west window is the warden's to open tonight).
```

```
Cut-Scene: Hold Hands        (ends the act, and the demo)
```
The title: "Hold Hands". Mom: "Places, girls. Hold hands. All the way through." The three of them in a row before the
door, Little Sister in the middle: "I'm in the MIDDLE. I'm always in the middle. It's the safest part of a sandwich." "Left
hand, right hand. Count of four. ...I'm not counting. I'm holding." Mom, with the coin in her fist, looks once round the
room, at the warden in the window with the mirror, at the sunset over the Inland Sea behind him, and prays: "Father, You
know where my son is, and I don't." "You knew at home. You knew in Nevada. You know now. Take us where You want us." "If
it's where he is, I'll never ask for another thing. ...That's not true. Amen." Little Sister: "Amen. Bye, poem man. Keep my
flashlight SAFE." "With both hands. Go, small one. The lady is waiting for you to go first." Big Sister: "...Thank you for
the stairs." Mom: "Your cue, girls." They walk into the light, hand in hand, the small one first; the coin goes with them.
The door holds for a breath after them, and closes as he lowers the mirror. Shinnosuke sits down on the floor with the
pink light in his hands: "She was not a ghost." "She was somebody's mother," "and she told the truth." And after a breath:
"...The dark is just dark." The tunnel. The card: "to be continued" (`edo.done`, `demo.done`), and the title. Skipped, the
same: the card always shows. It is not saved before (`save = false`): Continue after the end comes back to the last save
at rest, before the coin.

### Ledger rows

**Things that are carried** (the leg's part)

| Thing | Comes from | Who can hold it | Used for |
| --- | --- | --- | --- |
| Jinsuke's trowel | The hills (#34): Jinsuke gives it to them for his cousin | Mom (any of them, handed round) | #39: back into Tomezo's hand with Jinsuke's news; it stays with him |
| The bronze mirror | The hills (#34): Grandmother Sei gives it to Mom | Mom (handed back to Mom if a girl tries it on the hum) | #41: held in the sunbeam, its light on the hum: the door; then into the warden's hands, for Tomezo |
| Little Sister's pink flashlight | Little Sister's, from Act Three | Little Sister | #40: shown in the warden's face (a light with no fire) and lent to him; it stays with him ("Keep my flashlight SAFE") |
| The silver coin | Big Sister's (Act Four #10) | Big Sister; then Mom | #41: into Mom's hand ("The coin steers"); it goes through the door in her fist |
| A bucket of lime each | The castle approach, by the tub (#39) | each of the three (not an item: the scene's cut-outs, and the outfit) | the count: carried in at the gate; set down by the tubs in the keep |

**Clothes**

| Who | From | To |
| --- | --- | --- |
| all three | `edo` (O-Tami's travel clothes, hats on) at the castle approach | `edo-crew` (the plasterers' white head-cloths) from Tomezo's `dress` hook (#39) to the end |
| Mom | `edo-crew-mirror` while she holds the mirror up: at the top of the stairs as he kneels, and in the sunbeam with its light on the hum | `edo-crew` when she lowers it (he stands; the mirror to the warden) |
| Little Sister | `edo-lying` under the cherry, for a moment | her own (`edo` or `edo-crew`) again |

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| The cross on the round tile of the gate's gable ("Nobody knows who put it there." "Somebody did.") | #39, the castle approach | The cross in the door (#41) |
| Light opens them; more light, more door (Act Four, the sun shade) | #41, Big Sister's convex mirror ("The farther away you stand, the bigger the light.") | The doorway |
| The grandmother's mirror and its hidden cross (the hills) | #34 | #41: the cross in the door, and the mirror goes on to Tomezo, who will know whose it is |
| Little Sister's pink flashlight, too small to be seen in the morning sun (Act Four) | #40 | A light with no fire: the stairs, and the warden's dark |
| The lady of the keep: if you tell her the truth, she is kind | #40, the warden | #41: the lady is honest with the boy; "The dark is just dark." |
