# Act Six: By Your Grace (Japan, spring 1830): the puzzles

<!-- MERGE-20: new in round twenty. The design is briefs/out/edo-design.md; the act is js/content/acts/edo.js (act 7); its
three legs were built by SCENES-20A, 20B and 20C, and each wrote its part below. -->

Meanwhile, in another time: Mom, Big Sister and Little Sister come through the coin door expecting the Son, and step out
onto a beach at Yui, on Suruga Bay, in the spring of 1830 (Bunsei 13, the year of the metal tiger), in their own clothes,
in a country where foreigners landing are to be seized. The act is a journey west in three legs, each a place of its own
on the map of Japan (a woodblock travel map: `art/maps/edo/`): Yui; the hills north of Osaka, twelve days later by sea;
and Himeji, three days' walk on. The map takes the family only between the places of the leg they are in; a place of
another leg is drawn in, and Mom says why they are not going back (`maps.js`, a place's `leg` and `far`).

The rules the whole act keeps: nobody in the family lies (every option the player can pick for them is true, and the
comedy is in exactly true answers); the Japanese people speak as everyone in the game speaks, and a few of their own words
are glossed once; nothing frightening (the board is read once, the constable yawns, the warden's fright is comic); and the
hidden family under the storehouse is written with respect and warmth, never pity. Scripture is the King James text:
Psalm 139:9-10 at sea, Matthew 6:9 in the room underground, John 1:5 for the grandmother.

## The act at a glance

```
                    Cut-scene: Meanwhile, in another time (the beach at Yui, dawn)
                                          |
          +-------------------------------+--------------------------------+
          |                               |                                |
   #21 Where, And When            #22 Out Of Sight                  #23 Kihei's Table
   (Big Sister: a red hood,       (Mom: the board, the clerk,       (all: hungry, no money; pressed
    square-holed coins, a new      a baby, three kimonos; Little     sushi, freely given; a cat and a
    blue; the tiger year: 1830)    Sister keeps her boots)           mackerel; "Okage-sama de")
          +-------------------------------+--------------------------------+
                                          |
                     #24 West (the hens face west; Gonroku's ship; ask O-Masa)       GATE OF THE FIRST LEG
                                          |
                    Cut-scene: The Uttermost Parts (the ship by night; "Twelve days later")
                                          |
                     #25 Under The Cedars (the rain, the storehouse, the light under the floor)
                                          |
                     #26 Our Father (the room underground; the same prayer)
                                          |
                     #27 Charcoal, And A Kind Child (the constable; nobody lies; the egg)
                                          |    -> the mirror, the trowel, the castle's two stories
                    Card: "Three days later" (everyone else on the road going the other way)
                                          |
                     #28 Eight At The Gate (Tomezō's crew is three short; the cross on the tile)
                                          |
                     #29 A Light That Needs No Fire (the warden, the dare, the pink flashlight)
                                          |
                     #30 The Lady Of The Keep (the truth; the west window; the mirror's light)        THE GATE
                                          |
                    Cut-scene: Hold Hands (the wide door; the coin; the step; "to be continued")
```

The beats and the facts they make true (`js/content/acts/edo.js`): `edo.arrive` (`edo.arrived`), `edo.when` (#21),
`edo.dressed` (#22), `edo.fed` (#23), `edo.west` (#24: needs #22 and #23), `edo.sail` (the voyage: needs #24 and #21,
`edo.sailed`), `edo.hidden` (#25), `edo.trusted` (#26), `edo.mirror` (#27), `edo.walk` (the card, `edo.walked`),
`edo.inside` (#28), `edo.up` (#29), `edo.door` (#30), and the gate `edo.end` (the step: `edo.done`, and `demo.done`).
#21 to #23 are chains A, B and C, in any order. Every beat has a hint for each of the three; the long puzzles' hints
follow how far they have got (the act file's head lists the facts each stage reads).

Until #21 is solved the game never says the year: the map's band, its chip and the saved games show "Japan" alone (an
era's `dateAfter`, docs/DESIGN.md).

## Act Six, the first leg: Yui, on Suruga Bay

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
| One warm egg | Darlene, Act Four | Little Sister ("It's warm. It's MINE to keep warm.") | Shown to Kihei: "Keep your egg." Not yet: a constable on a path in the rain (#27) |
| Dad's pencil, the sticky note | Act Three | Whoever has them | Used on each other after #21: the sum written down (not needed) |
| Little Sister's pink flashlight | Act Three; given back to her at the hand-on | Little Sister | Not yet (#29) |

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| The Kirishitan board: silver for telling on anyone who prays to "the Kirishitan god" | #22, Sankichi reads it; "Then we pray quietly here." | The second leg: a hidden family under a storehouse, and a constable (#25 to #27) |
| "Nobody lies" | #22, the clerk: every answer true ("'From the east.' Mother. That was true.") | #27: the constable, and nobody lies |
| "Arigatō" | Sankichi, to Little Sister | The meal ("Husband. Your face."), the goodbyes ("Arigatō for the word."), and everyone after |
| "Okage-sama de": by your grace | #23, Kihei; Big Sister gives the act its name | The act's title, on its card |
| "Chickens KNOW." | Act Three, Act Four (Grandma Jolene's hens) | #24: every hen in Yui faces west |
| "I FIT." | Act Three, Act Four | #23: under the floor after the cat; and the storehouse's high window (#25) |
| The yellow boots | #22: "They're my BOOTS." | Kept the whole act, in every outfit; Sankichi wants to touch one (the LEFT one) |
| Psalm 139:9-10, "the uttermost parts of the sea" | The voyage, Mom at the stern rail; Big Sister gives the reference | "We're in the uttermost parts." "I know. So is His hand." |
| The baby asleep | #22 | Little Sister's grace (#23), and "Come back when the baby can talk." |

## Act Six, the second leg: the hills north of Osaka (#25 to #27, and the card "Three days later")

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
`edo.hidden`), the evening below (#26, until `edo.trusted`), the night (their own talks with Sei, Jinsuke and O-Rin, and
sleep), the morning (O-Rin's warning, `edo.watch`, until the constable has gone, `edo.constableGone`), and the sun on the
ladder after. It rains from the evening they come until he goes down the path with the egg (the rain on the path, its
drips from the eaves and puddles on the treads; in the storehouse the rain loud on the thatch, seen in the high window and,
when the door stands open, in the doorway); then the sun comes down the open trapdoor.

**The constable's way up the path** (#27) is a count of beats, not a timer: he is at the foot of the steps when O-Rin
sees him, climbs a step nearer each time one of the two things upstairs is done (the sacks, the pink light), and once all
three things are done (Mom below too) he climbs the last steps and knocks. Each step is seen: the storehouse looks out at
the path for a moment (the lead stays where she was), and he yawns. A look out of the door before the room is ready shows
him where he is.

### Puzzle structure

```
                 (the voyage: SCENES-20A's "The Uttermost Parts"; the card "Twelve days later", Osaka)
                                        |
                 #25 Under The Cedars (Little Sister; the path, the storehouse)
                     the door barred and nobody answering; calling out; the pipe in the hill: "The ground is PRAYING."
                     the high window: Mom lifts her; alone on the sacks; the bar
                     the mat with light at its edge: a trapdoor; "We should knock."; the light goes out, and comes back
                                        |   edo.hidden
                 #26 Our Father (Mom, then Little Sister; the room under the storehouse; a talk)
                     "We are charcoal-burners."; true things, and nothing asked; prayers, out loud
                     "Ten ni mashimasu..."; the altar; John 1:5 given and said back; O-Rin laughs once
                                        |   edo.trusted
                 the night: their own talks (the mirror, the cousin at Himeji, a light with no fire); sleep
                                        |
                 #27 Charcoal, And A Kind Child (all three; the room, the storehouse)
                     O-Rin's warning;  the sacks over the mat  |  the pink light off  |  Mom below
                     (any order: a step up the path for each of the first two; all three: the knock)
                     the constable let in; true answers; the egg: "Nothing here but charcoal and a kind child."
                                        |   edo.constableGone
                     the sun on the ladder: the grandmother's mirror, the cross in its light on the wall;
                     the mirror and the trowel to Mom; the castle's two stories: "That's a door."
                                        |   edo.mirror
                 Card: Three days later / Himeji ("Everybody else was going the OTHER way.")   edo.walked
                                        |
                 (the third leg: SCENES-20C's #28 Eight At The Gate)
```

The beats (`js/content/acts/edo.js`), each with its fact: `edo.hidden` (#25: lead Little Sister; it needs `edo.sailed`),
`edo.trusted` (#26: Mom and Little Sister), `edo.mirror` (#27: the family) and the card `edo.walk` (`edo.walked`). The
scenes' own facts the staged hints read: `edo.pipeHeard` and `edo.unbarred` (#25); `edo.sacksHid`, `edo.pinkOff` and
`edo.momBelow` (#27); and, with the change asked of MERGE-20 (ready.md), `edo.watch` and `edo.constableGone`.

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
Puzzle #25: Under The Cedars        (Act Six · Lead: Little Sister · the cedar path, the storehouse)
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
Puzzle #26: Our Father        (Act Six · Lead: Mom, then Little Sister · the room under the storehouse · a talk)
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
Puzzle #27: Charcoal, And A Kind Child        (Act Six · Leads: all three · the room, the storehouse)
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
| #25 | the pipe not heard | `hint.edo.hidden.mom` | `.bigsis` | `.lilsis` |
| | the door barred | `.mom.2` | `.bigsis.2` | `.lilsis.2` |
| | the mat (unbarred) | `.mom.3` | `.bigsis.3` | `.lilsis.3` |
| #26 | (one stage) | `hint.edo.trusted.mom` | `.bigsis` | `.lilsis` |
| #27 | the night (no `edo.watch`) | `hint.edo.mirror.mom.0` (new) | `.bigsis.0` | `.lilsis.0` |
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
| One warm egg | Darlene, out back (Act Four #11): Little Sister's since Nevada | Little Sister | #27: given to the constable's man, freely ("It's a good egg. I was going to hatch it."). He goes down the path with it in both hands. |
| Box of sushi | Kihei's (#23) | whoever the first leg left it with | #27, only if there were no egg: the rest of it, to the constable ("It's fish man's sushi. It's SQUARE."). The voyage eats it (SCENES-20A), so in the game as played the egg is always given. |
| Pink flashlight | Little Sister's own (Act Three) | Little Sister | The night: on in O-Rin's hands (a light with no fire). #27: left on, on the mats, for O-Rin: its light up between the floorboards. "Sorry, light.": off, and back in her pockets, for #29 (the warden). |
| Bronze mirror | Grandmother Sei's mother's, on its stand in the closet altar | Mom | #27's end: the cross in its light on the earth wall; sent with Mom, "where it can be held up in the light". For #30. |
| Plasterer's trowel | Jinsuke's cousin Tomezō's ("He has my trowel, or I his.") | Mom (in her sash) | For #28: give it back to Tomezō, and say Jinsuke is well. |
| Silver coin | Big Sister's, from Act Four | Big Sister | Not used here. For the end of the act. |

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| The warm egg, kept warm since Nevada | Act Four #11 ("It's MINE to keep warm.") | #27: "He was hungrier than it was ready to hatch." |
| "I FIT" | Acts Three and Four | #25: the storehouse's back window, a cupboard door's size: "I'm IN." |
| Knocking at doors, as manners | Mom, everywhere | #25: "It's still a door, sweetheart. Manners apply." A knock on a trapdoor is answered. |
| Little Sister's prayers out loud | The family's bedtime; O-Rin "has never said her prayers above a whisper" | #26: "Our Father..." answered with "Ten ni mashimasu..."; the night: O-Rin's prayer, a little louder; the goodbye: "...Goodbye. Out loud." |
| The grandmother's mirror ("Its face has not seen the sun in my lifetime.") | #26, on its stand; the night, her tree | #27's end: the cross in its light. #30: the door in the keep's sunset. |
| The cousin at Himeji, the trowel | The night, Jinsuke's tree | #27's end: the trowel; #28: Tomezō. |
| "Everybody else is going the other way." | #26, Big Sister on the pilgrims | The card: "Everybody else was going the OTHER way." |
| A light nobody lit, at the top of a building nobody may climb | #27's end, the castle's stories | #29 and #30 (the third leg). |
| Little Sister's pink flashlight | Act Three; the night here (O-Rin) | #29: lent to the warden. |

## Act Six, the third leg: Himeji (#28 to #30, and "Hold Hands")

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
         #28 Eight At The Gate (all three; the castle approach)
             Little Sister hollers Tomezo down his ladder; Mom gives back his trowel with Jinsuke's
             news; three hands short, three here: the head-cloths, a bucket each; the count
             -> eight went out, eight come in (edo.inside): the keep
                                        |
         #29 A Light That Needs No Fire (Little Sister; inside the keep)
             the warden at the stairs, his poems, the lady of the keep, no fire in a wooden keep;
             the pink flashlight shown, and lent: the lime may come up to carry it (edo.up)
             -> the climb, floor by floor, in the dark: "Two." ... "Six."
                                        |
         #30 The Lady Of The Keep (Mom; the top floor, at sunset)
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

The beats (`js/content/acts/edo.js`), each with the fact it makes true: `edo.inside` (#28: it needs `edo.walked`), `edo.up`
(#29), `edo.door` (#30) and the gate `edo.end` (Hold Hands, `edo.done`; with it the demo's end, `demo.done`). Each puzzle's
hint follows how far it has got, for each of the three (the facts the scenes set for it):

| Puzzle | Stage | The fact that moves it on | Mom's hint at that stage |
| --- | --- | --- | --- |
| #28 | Tomezo up his ladder | `edo.tomezoDown` | "The man in white up the ladder is Jinsuke's cousin. Your sister can reach him." |
| #28 | the trowel still carried | `edo.trowelBack` | "His own trowel back in his hand, and Jinsuke's name. He'll understand the rest." |
| #28 | not yet crew | `edo.crew` | "He's three hands short and we're three. Head-cloths and buckets, and we're crew." (never at rest: see #28's notes) |
| #28 | crew, at the gate | `edo.inside` | "Eight went out, eight go in. Carry lime, say nothing untrue. The count holds." |
| #29 | the warden not met | `edo.shinMet` | "The young man at the stairs fears the dark. Your sister has what he needs." |
| #29 | the light not shown | `edo.lightShown` | "He may carry no fire up. Your sister's flashlight isn't fire. Let her show him." |
| #29 | the light not lent | `edo.up` | "Lend him the light and we go up to carry it. That's a reason the lime may climb." |
| #30 | the truth not told | `edo.truth` | "He thinks I'm the lady. The lady asks for the truth. I'll give him mine first." |
| #30 | the west window shut | `edo.window` | "The west shutters are barred, and the bar is the warden's. Ask him." |
| #30 | the mirror not in the beam | `edo.letterbox` | "Sun behind me, the mirror in my hands, its light on the hum. Light opens them." |
| #30 | the letterbox, Mom not at the window | `edo.doorway` | "More light, more door. The farther I stand from the wall, the bigger the patch." |
| #30 | the doorway, the coin not in Mom's hand | `edo.door` | "The coin steers. Whoever has your brother's coin, I'd like it in my hand first." |

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
Puzzle #28: Eight At The Gate        (Act Six · Lead: all three · the castle approach)
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
Puzzle #29: A Light That Needs No Fire        (Act Six · Lead: Little Sister · inside the keep)
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
Puzzle #30: The Lady Of The Keep        (Act Six · Lead: Mom · the top floor)
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
| Jinsuke's trowel | The hills (#27): Jinsuke gives it to them for his cousin | Mom (any of them, handed round) | #28: back into Tomezo's hand with Jinsuke's news; it stays with him |
| The bronze mirror | The hills (#27): Grandmother Sei gives it to Mom | Mom (handed back to Mom if a girl tries it on the hum) | #30: held in the sunbeam, its light on the hum: the door; then into the warden's hands, for Tomezo |
| Little Sister's pink flashlight | Little Sister's, from Act Three | Little Sister | #29: shown in the warden's face (a light with no fire) and lent to him; it stays with him ("Keep my flashlight SAFE") |
| The silver coin | Big Sister's (Act Four #10) | Big Sister; then Mom | #30: into Mom's hand ("The coin steers"); it goes through the door in her fist |
| A bucket of lime each | The castle approach, by the tub (#28) | each of the three (not an item: the scene's cut-outs, and the outfit) | the count: carried in at the gate; set down by the tubs in the keep |

**Clothes**

| Who | From | To |
| --- | --- | --- |
| all three | `edo` (O-Tami's travel clothes, hats on) at the castle approach | `edo-crew` (the plasterers' white head-cloths) from Tomezo's `dress` hook (#28) to the end |
| Mom | `edo-crew-mirror` while she holds the mirror up: at the top of the stairs as he kneels, and in the sunbeam with its light on the hum | `edo-crew` when she lowers it (he stands; the mirror to the warden) |
| Little Sister | `edo-lying` under the cherry, for a moment | her own (`edo` or `edo-crew`) again |

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| The cross on the round tile of the gate's gable ("Nobody knows who put it there." "Somebody did.") | #28, the castle approach | The cross in the door (#30) |
| Light opens them; more light, more door (Act Four, the sun shade) | #30, Big Sister's convex mirror ("The farther away you stand, the bigger the light.") | The doorway |
| The grandmother's mirror and its hidden cross (the hills) | #27 | #30: the cross in the door, and the mirror goes on to Tomezo, who will know whose it is |
| Little Sister's pink flashlight, too small to be seen in the morning sun (Act Four) | #29 | A light with no fire: the stairs, and the warden's dark |
| The lady of the keep: if you tell her the truth, she is kind | #29, the warden | #30: the lady is honest with the boy; "The dark is just dark." |
