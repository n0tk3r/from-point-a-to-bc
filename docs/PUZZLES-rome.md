# Rome: puzzle document (first draft)

Act Two, the Son's act. Rome, the morning of the Ides of March, 44 B.C. A ten-year-old
has been put out of a temple with the door in time shut inside it. He gets back in, opens
the door exactly as far as a coin, and, once the coin's owner has said he may, tosses the
coin through.

It is laid out the way the project's puzzle-document method asks, and the way
[PUZZLES-the-present.md](PUZZLES-the-present.md) is: the characters, the puzzle
structure, the location layout, and then the cut-scenes and puzzles in order. Every
puzzle here is written as playable script, in `js/content/scenes/rome-steps.js`,
`rome-street.js` and `rome-temple.js`. Since round thirteen the act has three more places,
the Forum, the Capitol and across the Tiber (`rome-forum.js`, `rome-capitol.js`,
`rome-tiber.js`), and the talk of its seven new people is written as dialogue trees, in
`js/content/talk/rome.js`.

**Status: first draft.** The three places, the seven Romans, the five things, the ten
beats and the rule of the doors are the design (`briefs/LEVEL-rome.md`). The eighth
person, the date seller, and everything under "The family's faith" below were added on
7 October from `briefs/WEAVE.md`: fifty-five lines, no puzzle touched. The same evening
the author's two rules (`briefs/DATING.md`: how the game counts the years, and the
chickens) added four more lines, under "The chickens, and the years" below; again no
puzzle touched, and none of the fifty-five changed. What is
invention here, to keep, change or throw out: every line that is not an old one
(seventeen are kept word for word: the eleven the design names, his two old hints, and
the four looks at the coin); why each person wants what they want (the keeper's absent
boy, the senator's olive stain, the chickens that will not feed); the doorkeeper scoring
people out of three; the keeper feeding him on sight, which is "Step one: snacks" paid
off; the street boy's name, Walnut; the incense set down at the god's feet; the dog
asleep on the Forum, which he wants; and the three things in his pockets doing small
duty as wrong answers.

<!-- ROME-13W: round thirteen's status, and every part of this document marked "round thirteen" below -->
**Round thirteen: the bigger Rome, its first stage** (`briefs/ROME-13.md`, from the design
`briefs/out/rome2-design.md` and the author's thirteen decisions on it). Three new places on
the act's map: the Forum, the Capitol, and across the Tiber. Three new puzzles, one in each
chain, each adding a step to its chain and moving none, because the author asked to hold
off changing the puzzles he has played until he has played this: #10 Nobody Will Show Him
(chain A: the toga turns out to be a Gaul's, and the senator's own is on a lost Gaul in the
Forum), #11 Juno's Geese (chain B: the breakfast is up the Capitol with the keeper's boy,
behind the sacred geese), #12 Interest Is Extra Wishes (chain C: the coin was a mother's
wish; he asks before he throws it away, and pays it back). Seven new people, whose talk is
written as dialogue trees: the Gaul, Phyllis, Titus, the goose-keeper, Eleazar, Mariam and
Felix. The heart of the faith thread, Eleazar, the date seller's father-in-law, who prays
at his open window toward Jerusalem and waits for the one God has promised, with three new
quotations of Scripture; and the chickens' one more place, Mariam's hens. Six hundred and
six new lines; six re-worded (decision 12's, the keeper's four errand lines, Walnut's tip
about the breakfast); the seventeen kept lines as they were.

The decisions taken: the senator stays on the steps (his move to Caesar's door waits, and
with it Caesar's house and the design's Nine Hundred Senators); the washerwoman's mix-up
and the coin as Phyllis's wish are taken as added steps; the three quotations, yes; the act
does not wait for Eleazar; the Gaul tells Rome's joke on himself; the Ides ewe is talked of
and never seen hurt; the Egyptian queen is gossip only, and nobody in this stage says it;
seven of the design's fifteen new speakers now, the rest later; plain roles over people's
heads; the senator's toga plain white. What waits is under "What comes next", at the end.
The scenes were then built from this document (SCENES-13R1, the Forum and the steps;
SCENES-13R2, the Capitol and the street; SCENES-13R3, across the Tiber and the treasury),
and it now says what they do: where a builder had a choice to make, the card says what was
chosen. Every line is the writer's: the scene builders added none and changed none.

**What changes in the act he has played** (round thirteen), plainly. Each is an added step;
no puzzle he has played moves, and the old lines are said where they were:

1. **#2 Deliver It.** The first time the boy brings the senator his toga, it is the wrong
   one. On the steps, where he always was, the senator takes it, turns away to hold it up
   (his hand is empty: the people's rig has no toga to put in it), and finds it new and long
   enough to reach the ground twice: a Gaul's. The Gaul has his ("He will be in the Forum,
   lost."), and the boy is handed the Gaul's toga to carry. Brought the right one, he takes
   it as he always did, every line as it was but decision 12's.
2. **#1 Take The Toga.** Unchanged. Shown the Gaul's toga later, the washerwoman is
   briefly mortified: she turns away for a moment, and back.
3. **#4 Take The Breakfast.** The keeper feeds the boy as before, every line; then his
   errand is his boy Titus, who took the soothsayer's breakfast up the Capitol at first light,
   after the Ides ewe, and has not come back. The keeper no longer hands the breakfast over
   (the errand's four lines, three of his and the boy's answer, are re-worded under the same
   ids, and one of his is added, the ewe); Titus does, on the Capitol.
   Walnut's tip about the breakfast is re-worded to match.
4. **#5 Feed The Soothsayer.** One new first line when the breakfast has come down the hill
   ("Breakfast! It's been up a hill and past some geese."). The rest as before.
5. **#7 Borrow A Wish.** Unchanged, its four kept lines too; then Walnut says whose wish it
   was (two new lines).
6. **#9 Heads, Tails, Edge.** The toss waits for Phyllis's leave. Without it the boy stops
   himself ("Wait. This is Phyllis's wish. I'm not throwing somebody's wish through a door
   without asking."), and keeps the coin; with it, everything as before.
7. **The steps.** Two new ways out, the bottom edge into the Forum and the right edge up to
   the Capitol, each answering "Snacks first. My nose has spoken." until he has been to the
   street and worked out that it is B.C. The far view at the left is two things to click, the
   hill (the Capitol) and the Forum below it, each the same way as its edge: a look at either
   walks him to that edge first. The picture does not change.
8. **Decision 12.** One line re-worded (`rome.senator.toga.1`); the toga's inventory picture
   repainted plain white; the senator's toga drawn without its purple border.
9. **Hints.** The old hint for delivering the toga speaks for the first delivery, its words
   unchanged; the keeper's beat ends when he has said where his boy is; the new beats have new
   hints.
10. **The date seller** has one more line, once, after his blessing or at his goodbye: his
    wife's father reads in the house of prayer across the river; "Greet him for me."

Nothing else changes: #3, #6, #8, the act's opening, the cut-scene in the street, the end of
the act and its card. A game saved before round thirteen goes on: the steps it never had to
take count as taken (the three old scenes see to it as they are built), and a coin borrowed
in such a game is named Phyllis's by Walnut the next time the boy walks into the street.

<!-- MAP-15D -->
**Round fifteen: the map** (14 October; `briefs/MAP-15.md`). The game has a map screen now
(DESIGN.md, section 8, "The map, and the Timer"), and Act Two's map is a plan scratched with a
stylus into a wax tablet in its wooden frame: Saturn's steps in the middle, the street to the
left, the treasury behind the temple's doors, the Forum below, the Capitol up its hill to the
right, and across the Tiber at the lower left, beyond the river's bend and over the stone
bridge. A click on a place the boy has already been to takes him there, his portrait walking the
ways between, and he arrives as if he had walked in from the place before it; a place is there
to go to only once he has walked into it, so the map passes neither the doorkeeper nor the
steps' "Snacks first". Nothing in the act changed, but where one way out did something as he
left: across the Tiber, the old man's finishing his prayer while the boy is gone
(`rome.eleazarDown`, once `rome.sawTiber`) is set now by the scene's `leaving`, which runs
however he leaves, over the bridge or by the map, and the way over the bridge only goes. The
treasury does not let him go by the map once the coin has gone through (`rome.tossed`): the way
out is the way home. The act's check does in its stand-in for the engine what the engine's
`goto` does now (the scene's `leaving` first: one line in `check-rome.mjs`), and says exactly
what it said before; `play-tiber.py` says all 210 of the part's lines, and its record of every
way and every fact, `rome.eleazarDown` among them, is what it was, byte for byte.

Play it: `index.html?scene=rome-steps&lead=son` starts the act. In the full game it
follows Egypt, on a card that reads "Meanwhile, nearly nineteen hundred years later":
Dad's Egypt is about 1920 B.C. by the Bible's count, and 1921 B.C. to 44 B.C. is 1,877
years (`briefs/DATING.md`). The card is the Egypt act's (`egypt-chamber.js`).

How it is tested. `node briefs/out/check-rome.mjs` reads the act as it sits in the game,
walks every route on the engine's own walk map, compares every place with the painters'
measurements, and plays the scripts themselves through three walkthroughs on a stand-in for
the engine (`-v` prints them line by line). `python3 briefs/out/play-rome.py` plays the act
in the game itself, in a headless browser, by real mouse clicks, several ways round (since
round thirteen four, below), with the Hint button pressed at every stage, and visits as
games saved before earlier rounds would make them. On the way it goes through every branch
of the date seller, and everything else that was woven in, and checks what is on offer in
each list of things to say. It stops on any console error, and saves a picture of every
moment that matters in `briefs/out/shots-rome/`. Neither is a person playing it. Since
round three the check script also holds each scene's ways out at the edges of the picture
(where they lead, where he walks first, that the ground there can be walked to, that the
old ways out are kept), takes every one of them from every state it explores, and holds the
clickable shapes (no rectangles but the two painted boards; each cut-out and person named
for Show); and the play script leaves each scene by a click in the band along its edge and
comes back, after checking the arrow and the line that says where it goes, and turns Show
on in each scene for a picture, checking that everything is outlined.

<!-- ROME-13W -->
Round thirteen: each of the three scene builders wrote a play of his part, by real clicks
in the real game, and each ends NO PROBLEMS on the game with all three merged (and the
car's inside): `briefs/out/play-forum.py` (the steps' new ways both ways, closed and open;
the Forum's every thing; chain A both ways round, every wrong answer to the Gaul, the swap
wholly hidden behind the hoarding; chain C; the soothsayer's two first lines; a save and a
load; a game saved before round thirteen; the Hint button at every stage: 233 clicks),
`play-capitol.py` (the keeper first and the Capitol first; every thing on the Capitol; both
talks every way; every wrong try on the geese; the stomp from the goose-keeper's talk and
from the geese; the geese in the pen and staying; the street's new lines; Walnut's every
tip; the old act's saved games; less motion, and no moving things at all) and
`play-tiber.py` (the faith thread from the first sight to the last line, the three verses
letter for letter; leaving without waiting; Mariam; Felix with and without the lamp; the
treasury refusing the toss without Phyllis's leave, then the toss as it was: 210 lines of
the part, every one said). The check script and the act's own play were then rewritten for
the act as it is (the round's third phase, TESTS-13R): `play-rome.py` plays the act four
ways round by real clicks (the design's order; the coin first; leaving the Tiber without
waiting, with every wrong try; the old act's saved games played on), 1011 clicks, and with
the three part plays it says 1084 of the act's 1085 lines (not the look at Juno Moneta's
temple, which is not painted); `check-rome.mjs` reads the six scenes, the seven talks,
every way at the edges and the five verses. Both find nothing wrong. The seven talks were
also tested by the writer's own check, which plays each tree as the engine's `talk()` does,
down every branch, with every hook: every node it names exists, every line id exists, every
choice's line is the Son's, every line of every tree is said in some walk.

Where things are: every place in the three scene files is the painter's own
measurement of the finished picture (`layout.json` beside each picture in
`art/scenes/`), or was set by eye against the picture with the people standing in it
(the things the painters added after their lists were made). The clickable shapes were
traced again in round three, to hug their things for Show: they differ from the painters'
rough boxes on purpose, and the check script holds that each is still where the painter's is.
A few places differ from the painters' on purpose, and the check script lists each with
its reason: places to stand that the engine will not let anyone stand on; places that
lie under the inventory bar, which covers the bottom of the picture whenever the game
is waiting for a click; and two seated people, who are placed by the ground under their
hips. The date seller is in no painter's list: he was placed by eye (see his entry
under "The family's faith").

<!-- ROME-13W -->
The three new places are measured the same way, by their painters (PAINT-13R1 to R3), with
the marks the master brief fixes for them (`briefs/ROME-13.md`, "Measurements and formats").
Where a scene leaves a painter's number, its comment says why: on the Capitol the
goose-keeper stands 21 pixels behind his mark (at the mark he was drawn standing on the pen's
far fence, which is painted into the backdrop), and the pen's inside, where the geese run
to, is drawn in from the painter's: off its right-hand fence, so that no goose stands on a
rail, and off both ends of its near fence, so that no goose's head or tail shows past an end
of it (the second by the round's third phase, TESTS-13R); in
the Forum the boy talks to Phyllis from a step further out than the painter's stand for her
garlands (so that she can get up and go to her pole past him), the Tuscan street's area is
the street's shadowed opening on the ground (the painter's lay over Caesar's basilica and
the hill above it), and the pigeons are clicked bird by bird, as on the steps; across the
river the boy talks to Felix from a step east of the painter's stands round him (so that the
bollard does not hide his feet).

Puzzles are numbered within this act. The three of round thirteen follow the old nine, #10
to #12 (the design calls them NEW 2, 3 and 4; its NEW 1, Nine Hundred Senators, waits with
Caesar's house), and no old number moves.

## The idea of the act

Dad, in Egypt, makes tools out of what is in the car. The Son has no car. What he has
is legs, no fear, and a way of making friends in any century. So his act is **errands**:
everyone on the street has a use for a boy who can run, and each errand pays in the
thing he needs. Then comes the one clever thing, which is his own.

| | What he needs | Who has it | What they want first |
| --- | --- | --- | --- |
| **Chain A** | a clean tunic | the washerwoman | the senator's toga run up to the temple steps; since round thirteen, when it turns out to be a Gaul's, the right one got back from the Gaul in the Forum |
| **Chain B** | something for the god | the soothsayer | his breakfast, so that his sacred chickens will feed; since round thirteen it is up the Capitol with the keeper's boy, behind Juno's geese |
| **Chain C** | light, on a wall in the dark | the fountain, and the sun | nothing: a wish is borrowed. Since round thirteen it has an owner, Phyllis: he asks her before it goes through the door, and pays it back by carrying her lamp across the Tiber to her son |

**The rule of the doors**, the same in every era: a door in time stays where it once
opened, shut and invisible, and it hums. Light thrown on the place opens it, and the
more light, the bigger the door. The Son half knows this, because his key-ring
flashlight did it in the pyramid. Here he has a dead phone, a patch of morning sun on
the wrong part of the floor, and a new silver coin. A little light: a little door.

The player is never stuck on one thing. A, B and C are all open from the first minute,
in any order, and can be mixed. Nothing can be lost, used up wrongly or done too soon.
(Since round thirteen the Forum and the Capitol open once he has been to the street and
worked out that it is B.C.; across the Tiber lies beyond the Forum.)

---

# Act Two: Meanwhile

Rome, the Ides of March, 44 B.C. Morning.

## Characters

- THE SON: ten, lost, delighted; rates Rome out of ten and has an Operation for everything; wants his dad, and a snack, in that order on paper.
- THE DOORKEEPER: keeps the door of the treasury; scores what he sees out of three; wants nothing to change, ever.
- THE SOOTHSAYER: sits on the temple steps with his sacred chickens; has been telling Rome to beware the Ides of March since February; wants his breakfast, and not to climb fourteen steps.
- THE SENATOR: late for the Senate in yesterday's toga; has a magnificent speech about drains; wants his clean toga, and to be looked at. (Since round thirteen the first toga brought him is a Gaul's.)
- THE SNACK-BAR KEEPER: feeds everyone and is owed by everyone; has not drawn breath in eleven years; wants his boy Titus home from the Capitol, and the soothsayer's breakfast with him (before round thirteen: wanted the breakfast taken up the street).
- THE WASHERWOMAN: runs the laundry on "first" and "then"; cleans cloth the Roman way and sees nothing odd in it; wants the senator's toga off her hands. (Round thirteen: at first light, in the dark, a big man asked her for "the senator's toga", and she gave him the senator's.)
- THE STREET BOY ("Walnut"): the Son's age, best at nuts on the street; cannot take his eyes off the light-up sneakers; knows whose wish is in the fountain; wants a friend, and is the act's hint-giver.
- THE CLERK: counts the Roman People's silver, twice, by lamplight; loses count whenever anyone speaks; wants to reach a number.
- THE DATE SELLER: a Jew from Judea, about fifty, selling dates from Jericho at the kerb; courteous, humorous, unhurried, nobody's fool; keeps the seventh day, prays toward Jerusalem, sends his half-shekel home; wants nothing from the boy, and is waiting for someone. He is part of no puzzle. His wife's father reads in the house of prayer across the river.
<!-- ROME-13W: the seven of round thirteen (their pages are in CHARACTERS.md) -->
- THE GAULISH SENATOR (Gaius Iulius Litumarus): a Gaul of Nemausus in the Province, made a senator by the dictator, at his first meeting, in a toga far too short for him (the senator's, handed him in the dark); careful, dignified, dry; tells Rome's joke about Gauls before anybody else can; wants somebody, anybody, to tell him where the Senate meets today.
- THE GARLAND SELLER (Fannia Phyllis): a Greek freedwoman selling violets, laurel and myrtle at the foot of Castor's temple on the busiest morning of her spring; fast patter, sharp with fools, soft about her son; threw a new silver coin in the fountain at first light with a wish for him; wants to give him her little clay lamp before he sails for Corinth, and cannot leave her baskets.
- THE KEEPER'S BOY (Titus): eleven, the snack-bar keeper's son, who talks like his father without stopping for breath; followed the Ides ewe up the Capitol with the soothsayer's breakfast, and is sitting on a statue's base among the kings with the sacred geese all round its foot, on purpose, mostly; wants to get down without saying he is stuck.
- THE GOOSE-KEEPER (Titus Rubrius Anser): feeds the sacred geese of Juno for the Republic, and his name means goose; mournful, devoted; tells the story of the night the geese saved the city to anybody, and nobody listens; wants nothing to happen to his geese, and somebody to listen.
- THE OLD MAN (Eleazar): the date seller's wife's father, a Jew of Jerusalem brought to Rome as a captive nineteen years ago, and freed; prays at his open window toward Jerusalem, then reads on the bench by the house of prayer; slow, warm, grave, with a dry humor; is waiting for the one God has promised. He is part of no puzzle.
- THE GIRL (Mariam): about eight, his granddaughter, the date seller's daughter; certain about everything, especially hens; her hens have stood in a row since first light looking over the river at the city, and will not eat; wants them to finish looking. Part of no puzzle.
- THE BOATMAN (Gaius Fannius Felix): Phyllis's son, sunburnt, cheerful, impatient; carries bales between the landing and the barge across the Tiber; his name is down for Corinth; wants to sail, and does not know his mother has a lamp for him.

## Puzzle structure

<!-- ROME-13W: the chart as round thirteen leaves it (the three new puzzles in their chains) -->
```
                         Cut-scene: Not the rest stop
                                      |
                Cut-scene: Before Christ (the street; opens the Forum and the Capitol)
                                      |
        +-----------------------------+------------------------------+
        |                             |                              |
 #1 Take The Toga            #4 Take The Breakfast            #7 Borrow A Wish
   (the street)                 (the street: his boy             (the street)
        |                        has it, up the hill)        Walnut: it is Phyllis's
 #2 Deliver It: the turn              |                              |
   (the steps: a Gaul's!)     #11 Juno's Geese                       |
        |                        (the Capitol)                       |
 #10 Nobody Will Show Him             |                              |
   (the Forum: the Gaul)      #5 Feed The Soothsayer                 |
        |                        (the steps)                         |
 #2 Deliver It                        |                              |
   (the steps)                        |                              |
        |                             |                              |
 #3 Collect The Tunic                 |                              |
   (the street)                       |                              |
        |                             |                              |
        +--------------+--------------+                              |
                       |                                             |
            #6 Three Out Of Three                                    |
          (the steps: the doorkeeper)                                |
                       |                                             |
                       +----------------------+----------------------+
                                              |
                                        #8 Tiny Sun
                                        (the temple)
                                              |
                              #12 Interest Is Extra Wishes      <- any time after #7
                   (the Forum: Phyllis; across the Tiber: Felix; the Forum again)
                                              |
                                  #9 Heads, Tails, Edge          the gate
                                        (the temple)
                                              |
                     Cut to: "Meanwhile, about two thousand years later"
```

Goal of the act: **get back to the door, and find out what it does with a coin.** Two
chains of errands meet at the doorkeeper; the third is one borrowed coin that waits
for him inside, and since round thirteen it has an owner, whose leave he gets before he
throws it away. Easy on purpose, for a ten-year-old lead: every step is told to him by
someone, in character, before he can be stuck on it. The one step nobody tells him is
the last idea, the coin as a mirror, and he has the pieces of it in his own words. Two
of the three new steps are solved by something said: the Gaul's question by what the
senator said about his speech, and the geese by the goose-keeper's one story.

The beats (`js/content/acts/rome.js`), in the order the story file lists them: the Hint
button speaks for the first one that is open. As round thirteen leaves them:

| Beat | Chain | What | Where | Needs | Sets | Hint |
| --- | --- | --- | --- | --- | --- | --- |
| `rome.arrive` | | Not the rest stop | the steps | `egypt.ready` | `rome.arrived` | |
| `rome.toga` | A | Take the senator's clean toga from the washerwoman (#1) | the street | `rome.arrived` | `rome.hasToga` | `hint.rome.toga` |
| `rome.wrong` | A | Deliver it: it is not his toga (#2, the turn) | the steps | `rome.hasToga` | `rome.wrongToga` | `hint.rome.delivered` (its words as before) |
| `rome.gaul` | A | Show the Gaul the way, and swap togas (#10) | the Forum | `rome.wrongToga` | `rome.swapped` | `hint.rome.gaul` |
| `rome.delivered` | A | Deliver the right toga to the senator (#2) | the steps | `rome.swapped` | `rome.delivered` | `hint.rome.delivered2` |
| `rome.tunic` | A | Go back for the tunic she promised (#3) | the street | `rome.delivered` | `rome.hasTunic` | `hint.rome.tunic` |
| `rome.breakfast` | B | Ask the keeper for the soothsayer's breakfast (#4) | the street | `rome.arrived` | `rome.knowsBoy` | `hint.rome.breakfast` (its words as before) |
| `rome.geese` | B | Get the keeper's boy, and the breakfast, away from Juno's geese (#11) | the Capitol | `rome.knowsBoy` | `rome.hasBreakfast` | `hint.rome.geese` |
| `rome.incense` | B | Feed the soothsayer, and be trusted with his incense (#5) | the steps | `rome.hasBreakfast` | `rome.hasIncense` | `hint.rome.incense` |
| `rome.inside` | A+B | Past the doorkeeper: in the tunic, with the incense (#6) | the steps | `rome.hasTunic`, `rome.hasIncense` | `rome.inside` | `hint.rome.inside` |
| `rome.coin` | C | Borrow a wish from the fountain (#7) | the street | `rome.arrived` | `rome.hasCoin` | `hint.rome.coin` (kept) |
| `rome.spark` | C | Bounce the sunlight off the coin onto the place that hums (#8) | the temple | `rome.inside`, `rome.hasCoin` | `rome.doorOpen` | `hint.rome.spark` |
| `rome.wish` | C | Ask Phyllis about her wish, and take her lamp to her son (#12) | the Forum | `rome.hasCoin` | `rome.hasLamp` | `hint.rome.wish` |
| `rome.felix` | C | Find Felix at the barges across the Tiber (#12) | across the Tiber | `rome.hasLamp` | `rome.felixWord` | `hint.rome.felix` |
| `rome.granted` | C | Tell Phyllis; she lets him keep the coin (#12) | the Forum | `rome.felixWord` | `rome.wishGranted` | `hint.rome.granted` |
| `rome.toss` | gate | Toss the coin through the door (#9) | the temple | `rome.doorOpen`, `rome.wishGranted` | `rome.tossed` | `hint.rome.toss` (kept) |

(Until round thirteen the story facts were `rome.arrived`, `rome.hasToga`, `rome.delivered`,
`rome.hasTunic`, `rome.hasBreakfast`, `rome.hasIncense`, `rome.inside`, `rome.hasCoin`,
`rome.doorOpen`, `rome.tossed`: they keep their meaning.)

## Location layout

```
+------------------------------------------------------------------------------+
| THE STEPS OF THE TEMPLE (rome-steps)                 he starts here          |
|                                                                              |
|  the far view: THE HILL    THE DOORS (open)  <- THE DOORKEEPER, in the way   |
|  (the Capitol), and THE    columns                                           |
|  FORUM below it            notice board   fourteen steps                     |
|  a handcart, a dog asleep  THE SOOTHSAYER and his SACRED CHICKENS            |
|  left edge:      ALTAR   tripod                           right edge: up the |
|  to the street   THE SENATOR (until his toga comes)      hill to the Capitol |
|                  pigeons  carved stone       bottom edge: into the Forum     |
+------------------------------------------------------------------------------+
        |  up the street (top edge) / to the street (left edge)   | through the doors
+-----------------------------------------------+  +---------------------------+
| THE STREET (rome-street)                      |  | INSIDE THE TEMPLE         |
|                                               |  | (rome-temple)             |
|  far end: the Forum, small and sunlit         |  |                           |
|  WASHING LINES overhead, a SMALL TUNIC on     |  |  THE STATUE, feet tied    |
|  the low one    apartments, a songbird, a cat |  |  offering bowl            |
|  SNACK BAR, sign, price list  writing  shrine |  |  THE PLACE THAT HUMS      |
|  THE KEEPER            on the walls FOUNTAIN  |  |  (left wall, in shadow)   |
|  laundry basket                               |  |  chests, a cat      rack  |
|  THE WASHERWOMAN   stepping stones  THE DATE  |  |  THE CLERK at his table   |
|                    THE STREET BOY    SELLER   |  |  SUNLIGHT ON THE FLOOR    |
|                           jars, a cart wheel  |  |  out: behind us (bottom)  |
+-----------------------------------------------+  +---------------------------+
```

Three scenes. The street and the steps are open from the start; the temple is shut
until #6, and open to him ever after. (Six since round thirteen: the next section.)

### The six places, and the ways between them (round thirteen)

<!-- ROME-13W -->
```
                          THE CAPITOL (rome-capitol)                        new
                                 |  ^
            its bottom edge: down |  | the steps' right edge: "up the hill to the Capitol"
                 to the steps     v  |
 THE STREET  <-- the steps' left edge --  THE STEPS (rome-steps)  -- the doors -->  THE TEMPLE (rome-temple)
 (rome-street) -- its top edge ------->        |  ^
                                               |  | the Forum's top edge: "back to the steps of Saturn's temple"
               the steps' bottom edge:         v  |
               "into the Forum"           THE FORUM (rome-forum)                     new
                                               |  ^
                its left edge: "down the      |  | across the Tiber's bottom edge: "back over the stone bridge"
                Tuscan street, over the river" v  |
                                          ACROSS THE TIBER (rome-tiber)               new

        later: CAESAR'S HOUSE (rome-house), off the Forum's bottom edge, "along the Sacred Way to the chief priest's house"
```

```
+------------------------------------------------------------------------------+
| THE FORUM (rome-forum), from its east end, looking west          new         |
|                                                                              |
|  over everything, the Capitol: JUPITER'S TEMPLE and its GOLD ROOF, MONETA    |
|  on the other summit, the RECORD OFFICE between                              |
|  far end: SATURN'S TEMPLE, small (his own; the door guy "a dot"), and the    |
|  SPEAKERS' PLATFORM before it, not yet finished                              |
|  left: CASTOR'S TEMPLE, JUTURNA'S SPRING     right: PAULLUS'S BASILICA, its  |
|  before its steps, and PHYLLIS on her        shops; before it the HOARDING   |
|  stool among her GARLANDS; the mouth of      round the HOLE where the senate |
|  the TUSCAN STREET (to the river); CAESAR'S  house was, with its gateway and |
|  BASILICA, in its SCAFFOLDING                THE GAUL before it; the CRANE   |
|  the square: the PUTEAL, a moneychanger's TABLE, STATUES on three columns,   |
|  PIGEONS, and an empty statue base at the front                              |
|  top edge: back to the steps   left edge: over the river   bottom: (later)   |
+------------------------------------------------------------------------------+

+------------------------------------------------------------------------------+
| THE CAPITOL (rome-capitol): the precinct of Jupiter Best and Greatest  new   |
|                                                                              |
|  right, far off: JUPITER'S TEMPLE (its NAME, its GOLD ROOF, its DOORS);      |
|  before its steps the great ALTAR, the dictator's CHARIOT, and his bronze    |
|  man on the WORLD                                                            |
|  (Moneta, on the hill's other summit, is out of sight behind the temple)     |
|  middle: the KINGS (OLD BRUTUS with his sword; the dictator's SHINY NEW      |
|          STATUE); TITUS on top of the middle base, and JUNO'S GEESE          |
|          round its foot                                                      |
|  left: ROMULUS'S HUT; the geese's PEN, THE GOOSE-KEEPER behind it; the       |
|        parapet, and over it the VIEW: the JANICULUM, the RIVER and the       |
|        ISLAND, POMPEY'S THEATER on the plain                                 |
|  front right: the bronze TABLETS on their posts                              |
|  bottom edge: down the hill to the steps (the gate is behind us)             |
+------------------------------------------------------------------------------+

+------------------------------------------------------------------------------+
| ACROSS THE TIBER (rome-tiber): below the stone bridge, looking downstream new|
|                                                                              |
|  left: the RIVER, the LANDING and its steps, the BARGE, the BALES, and FELIX |
|        at work between them; the FAR BANK                                    |
|  middle: the WELL in the little square; the ROAD along the river to the      |
|          GARDENS' wall                                                       |
|  right: ELEAZAR'S HOUSE (its DOOR and DOORPOST, the WASHING, his upper       |
|         WINDOW and the old man praying in it); the HEN YARD and its FIG TREE,|
|         MARIAM and her HENS in a row; the HOUSE OF PRAYER and its BENCH      |
|  bottom edge: back over the stone bridge to the Forum                        |
+------------------------------------------------------------------------------+
```

| From | Way | To, arriving at | The line says | Open |
| --- | --- | --- | --- | --- |
| the steps | bottom edge (S), and the Forum in the far view | the Forum: at the far end, the foot of Saturn's steps (`fromSteps`), small under his temple; he walks a good way down the square | Go into the Forum | once `rome.knowsBC`; before, "Snacks first. My nose has spoken.", and he stays |
| the steps | right edge (E), and the hill in the far view | the Capitol: at its gate, behind us (`fromSteps`); a step up into the precinct | Go up the hill to the Capitol | the same |
| the steps | left edge (W); the doors | the street; the treasury | Go to the street; Go through temple doors | as before |
| the Forum | top edge (N), and the far temple of Saturn | the steps: at the bottom edge (`fromForum`); he walks up out of the band | Go back to the steps of Saturn's temple | always |
| the Forum | left edge (W), and the mouth of the Tuscan street | across the Tiber: off the bridge, behind us (`fromBridge`); a step onto the lane | Go down the Tuscan street, over the river | always |
| the Forum | bottom edge | (later: Caesar's house) | | not in this stage: plain floor |
| the Capitol | bottom edge (S) | the steps: at the right edge (`fromCapitol`); he walks in, clear of the carved stone | Go down the hill to the steps | always |
| across the Tiber | bottom edge (S) | the Forum: a step out of the mouth of the Tuscan street (`fromTiber`); he walks out onto the square | Go back over the stone bridge | always |

On the steps the far view is two things to click, each the same way as its edge: the hill,
"Capitol" ("Walk to Capitol": "The road up there goes round the back of this temple. Rome
hides its stairs."; once he has been up, "I've BEEN up there. The geese say hi."), and the
Forum below it ("Walk to Forum", its old looks). A look at either walks him to its edge
first, and he says it there (SCENES-13R1's choice: each is the same way as its edge); at
the right edge his words are lifted over the soothsayer's head, which they would lie across.
The picture of the steps does not change. Where a thing in a new picture is also a way out
(the far temple of Saturn, the mouth of the Tuscan street), using it takes that way; the far
temple is looked at from where he stands ("That's MY temple, way down there."). The ways at
the edges of the act are drawn as a map on the storyboard page (`tools/storyboard.html`,
"Maps"), from the scenes' own data: the treasury above the steps, the street to the left,
the Capitol to the right, the Forum below, and across the Tiber below the street. The game
itself has no map screen (DESIGN.md, section 14, asks the author whether he wants one).
<!-- MAP-15D --> It has one since round fifteen (above, "Round fifteen: the map"): the wax
tablet, laid out as the storyboard's map is, with the Capitol up its hill and across the Tiber
beyond the river's bend.

### The ways between the scenes: the edges of the picture (round three)

The author, on the evening of 7 October: a click at the top or the bottom of the picture
should be enough to walk to the next scene, and the same at the sides if a scene lies that
way. So each scene names the way out that lies off an edge of its picture (`edges` in the
scene file). A click on the ground in the band along that edge (the top 60 pixels, the
bottom 52, the sides 44) walks the Son to that way out and through it; there the pointer
is an arrow pointing out of the picture, and the line at the bottom of the screen says
where it goes. Anything that can be clicked in the band still wins over it. The ways out
that were there before are all kept.

| Scene | Edge | Leads to | The line says | He walks first to | The way out that was there before, kept |
| --- | --- | --- | --- | --- | --- |
| The steps | left | the street | "Go to the street" | the painter's way out at the left edge of the pavement, behind the laurel (34, 470) | "the street", that way out itself: now the painter's 40 pixels again (it was widened to 64 to be easier to find; the whole left edge does that now) |
| The street | top | the steps, in the Forum | "Go up the street to the Forum" | the far end of the street (400, 338), whatever part of the top was clicked | "the Forum", the gap at the end of the street and the roadway up to it |
| Inside the temple | bottom | the steps | "Go out to the steps" | the doors behind us (400, 594) | the door leaves at both sides of the picture, and the bottom edge itself ("the steps") |

The steps have no way out at the top: the temple's doors are in the middle of its front
wall, and stay a thing to click on (they are the doorkeeper's gate, #6). No other edge of
the three pictures leads anywhere: the street runs on toward us and the Forum lies off to
the left of the steps, but the act does not go there. A game saved just after the coin
went through goes home from the temple, by the bottom edge as by the door leaves.

<!-- ROME-13W -->
Since round thirteen the steps have two more ways out, at the bottom (into the Forum) and at
the right (up the hill to the Capitol), and each new place has its own: the table in the
section above.

### What Show outlines (round three)

Show (the button, or holding H) outlines each thing that can be clicked, with a light line
and a glow, and fills nothing; each way out at an edge gets an arrow. So every clickable
area hugs its thing, a few pixels outside its edge, traced from the painter's pictures and
cut-outs and from the figures the game draws. The cut-outs (the fountain, the
small tunic, the jars and the cart wheel; the altar, the tripod, the carved stone; the
clerk's table, the door leaves, the near brazier; since round four the cat on her sill)
and every person are outlined by their own pictures; the washing, which since round four
is thirteen pieces that each stir by themselves, by its own hugging shape. Things that
come in several pieces are several things to click, which all say the same: the three
stepping stones, the ten pigeons on the pavement (since round four: each outlined by the
bird itself, wherever it is), the nine bronze tablets of the laws in the temple. The place
that hums has nothing painted on it, so its outline is a ring round the spot on the wall
(and the little door's, when it is open, a smaller ring). The price list and the shrine
are boards painted on the wall, and stay rectangles.

### The pigeons, and everything else that moves (round four)

Nothing that moves by nature is painted still any more (briefs/ROUND-4.md): the altar's
smoke rises and leans with the morning air, the coals breathe, pigeons potter and peck on
the pavement, the steps and the temple's gutter, swallows cross the sky, the laurel at the
front and the washing in the street stir, the fountain runs, the cat's tail swings, the
lamps and braziers flicker. None of it is a thing to click, but for one: **the pigeons**.
The ten on the pavement (eight on the open pavement right of the altar, and two by the cart's shade) are
each a thing to click wherever they are, and all say the same as the five painted ones
did: looked at, "Pigeons. The exact same pigeons as at home..."; **Chase**, and he takes
one quick step at the one he clicked, they all go up and land again a little way off (or
fly off over the roofs and come back later), and he says, as before, "I'm not chasing them.
I chased one at a rest stop once and Dad had to apologize to a truck." Walking near them
sends them up too. Nothing else about the act changed for a player: the people who now get
up and walk about by themselves (below) are always back on their marks before anyone talks
to them.

**The people's own lives.** In the street the snack-bar keeper goes along behind his counter
to his pots or his stove, the washerwoman to her basket or out under her lines, the street
boy up off the kerb to the fountain or a step into the road, the date seller a few steps up
the pavement or along the kerb; on the steps the senator paces, the soothsayer gets up
(slowly) to look at his birds or along his step, and the doorkeeper keeps the door (small
movements only); in the temple the clerk goes to his rack or along behind his table. One at
a time, each in their own time, and never while a script has the stage.

**The three new places** (round thirteen) move in the same way, as their painters marked
them. In the Forum: the thread of smoke from the Ides offering, far up on the Capitol; the
water coming into Juturna's spring, its rings and the light on it; pigeons on the square
(the seven near ones are things to click, bird by bird, as on the steps: "Chase"; the three
far up the square are not); swallows over the hill; the moneychanger's awning stirring; and
the crane's great wheel, still most of the time, turning two turns now and then (every half
a minute or so), with a little pale dust where a block is set down after it (with less
motion the wheel stays still). On the Capitol: the last of the morning's smoke from the
great altar, and a few coals in its ash; the geese; two kites wheeling high over the
precinct; threads of smoke from the city below; light on the river round the island. Across
the Tiber: the sun's glints on the river, drifting downstream; ripples along the barge and
at the landing's steps; the barge riding the water at its moorings, a pixel up and down;
Mariam's five hens in their row, each in her own colouring and her own place; the washing
stirring on its line; a cooking fire's smoke behind the houses; swallows over the river.
New sounds: the geese's honk, their cry as they run, and their hiss; and across the river
the act's own quiet tune (`tiber`), which stops while the old man talks with the boy, so
that the river is heard (very softly: SCENES-13R3 measured it beside its neighbours).

Their people live by themselves too: the Gaul walks along the hoarding and back, and out
toward the middle of the square, tugging the short toga down, looking up at the crane,
folding his arms, asking the air and shrugging; Phyllis gets up now and then to hang a
garland on her pole and sits again, and sitting she weaves, sniffs a violet, counts her
coins and looks across the square; Titus, high on his base, only waves, peeks into the cloth
and pretends to be a statue; the goose-keeper walks a few steps along the back of his pen
(looking over at the base, or into the pen once the geese are in it), shakes his basket,
leans on his stick, counts his geese and sighs; the old man at his window lifts his head
now and then, his lips moving, and on his bench unrolls his scroll, reads with a finger,
strokes his beard and looks up across the river; Mariam goes to a corner of her yard and
back, scatters grain nobody eats and counts her hens; Felix works between the landing and
the barge's side. Where somebody stands farther back with his face just where the boy's
words would go, the words are lifted over his head (the sprite flag `clear`): Titus and the
goose-keeper on the Capitol, the old man on his bench, and, since round thirteen, the date
seller in the street (Walnut's long new tips lay across his face).

## Cut-scenes and puzzles

```
Cut-Scene: Not the rest stop        (opens the act)
```
The foot of the temple steps. The doorkeeper, at the top: "And stay out. The treasury
of the Roman People is not a nursery." The Son looks about him: this is NOT the rest
stop, everyone is wearing a bedsheet, ten out of ten. Then back at the temple: "The
humming door let me out INSIDE that building. Then it shut. Not even a goodbye hum."
The big guy carried him out by his backpack, like luggage. "Okay. Operation Find Dad.
Step one: snacks. Step two: also Dad. Step three: get back in there. I'm adding a step.
It's my operation." And he turns to the left edge of the picture, where the street is:
"Step one is THAT way, past the bush. My nose is never wrong about snacks."
*Plants:* the door is inside, and shut (#8). Step one, snacks (#4). Fourteen steps (#5).
The way to the street, which is behind the laurel and easy to miss (since round three the
whole left edge of the picture is that way, and his nose has already pointed there).
*Also:* the three things in his pockets arrive with him, without fuss: a dead phone, a
quarter, half a pack of gum. He plays the act alone: Dad is still in Egypt, standing at
his door, and there is nobody to switch to.
*Since round thirteen* (ROME-13W): the steps' bottom edge (into the Forum) and right edge (up
the hill to the Capitol), and the far view's two halves, answer "Snacks first. My nose has
spoken." (`rome.steps.closed`), and he stays, until he has been to the street and worked
out that it is B.C.

```
Cut-Scene: Before Christ        (the first time he walks into the street)
```
He comes down the street between the stepping stones. "Whoa. A whole street of snacks
and laundry." From the snack bar, the keeper, crying his wares: "Hot sausage, hot bread,
old silver, new silver, the new has Caesar's nose on it, I take every nose!" The boy
looks round. "Caesar? JULIUS Caesar? Big Sis has him on her timeline. Before the red
mark. That whole side is B.C." And then to nobody: "B.C. Before Christ. ...So Jesus
hasn't been born." "So it's before Christmas. Not this Christmas. EVERY Christmas. All
of them. The FIRST one." "Operation Don't Wreck Anything. I mean it. I've never been in
front of anything this big." And then, being ten: "Step one, I can SMELL you."
*Plants:* everything he will say "Not yet." about (the coin, #7; the senator; the road).
The red mark on Big Sister's timeline, which the player sees in Act Three. What B.C.
means, which is what makes Little Sister's "EARLY" land in Act Four.
*Why here:* the era card has just told the player "Rome, 44 B.C."; the boy has to work
it out, and this is the earliest moment every way through the act passes. Whatever he
does first in the street, he knows by then. (A game saved in the street before this was
written hears the cry the next time he walks in: `rome.knowsBC` is its own fact.)
*Since round thirteen* it is also what opens the Forum and the Capitol (`rome.knowsBC`), so it
still comes first in every way through.

```
Puzzle #1: Take The Toga        (Rome · the street · the washerwoman)        chain A
Needs:        nothing
Setup:        The washerwoman has a senator's toga, dry and folded, and nobody to carry it:
              she cannot leave the tubs. Overhead the washing lines cross the street, and on
              the low one hangs a tunic the size of a boy.
Wrong tries:  Take the tunic off the line   -> "Hands off the line, child. Those are counted."
              Dunk the toga in the fountain -> "The laundry lady has ARMS. I've seen them."
              Give the toga back to her     -> "Not to ME. To HIM. Up the street, at the temple
                                              steps, the color of a plum."
Solution:     Talk to her. She looks him over ("A pouch on the belly, and a hood with no head in
              it. Whoever dresses you enjoys a joke.": PASS-17R, round seventeen, for he wears no
              cap), asks if he can run, and makes the offer:
              take the toga to the senator at the temple steps, "and I will lend you a proper
              tunic for the day." "Deal. Operation Bedsheet Delivery. I'll carry it by the corners."
Gives:        The senator's toga.
Teaches:      That people here pay for errands, and that she is where tunics come from.
Hints:        Hint button: "The door guy wants a kid in a clean tunic. The laundry lady on the
              street has a whole line of them." The street boy: "A clean tunic? The laundry woman
              has a hundred. And never anybody to run things up the street." The senator: "The
              washerwoman by the fountain has had my best one for three days. THREE."
Plants/pays:  Plants the tunic on the line (#3) and "by the corners" (below).
Notes:        Ask her how she gets them so white, and she tells him: trodden in the tubs with stale
              urine. "You wash clothes in PEE. That's the best fact I've ever heard. Ten out of ten.
              ELEVEN. My sister's going to be so mad I knew it first." If he is holding the toga:
              "...Wait. This bedsheet I'm holding..." "Was rinsed. Twice." "I'm going back to the corners."
              Round thirteen (ROME-13W): unchanged, but the toga she hands over is, unknown to her,
              the Gaul's (#2's turn). Shown the Gaul's toga: "Laundry lady? This isn't the senator's.
              It's a Gaul's. It reaches the ground TWICE." "...At first light a big man came asking for
              'the senator's toga'. In the dark. I gave him the senator's." She turns away from him:
              "Twenty years on first and then, and I gave the wrong first." And back, brisk again:
              "Well. Standing here will not swap them. Find the Gaul, child. Big, lost, knees out. Go."
              Again: "I KNOW, child. Find the Gaul. And never say a word of it to my sister." (The
              lamp, shown her, has a line of its own.)
```

```
Puzzle #2: Deliver It        (Rome · the steps · the senator)        chain A
Needs:        #1. Since round thirteen it is played twice: the first time, the toga is the wrong one
              (the turn, below); the delivery itself needs #10.
Setup:        A senator stands at the foot of the steps in yesterday's toga, late for the Senate,
              which meets today in the hall beside Pompey's theater. There is an olive stain. He
              will not be seen with it.
Changed:      THE TURN (round thirteen; the author's decision 2). The first time the boy brings it:
              "Delivery! One senator's bedsheet, fresh from the laundry lady. Folded by a
              professional." The boy holds it out, and the senator takes it: "At LAST. Three days.
              Give it here." He turns from the boy to shake it out and holds it up at arm's length:
              "...This toga is new. It has never been to the Senate. It has never been to ANYTHING."
              "And it reaches the ground. Twice." He turns back: "Maybe it's a growing toga. Mom buys
              all my clothes big. I'm still growing into my HOODIE." "The Gaul! The laundress fulled a
              toga for one of the dictator's new Gauls. He has MINE." He holds the enormous one out
              to the boy: "He will be in the Forum, lost. They are always lost.", and the boy takes it:
              "Okay. Find the lost Gaul, swap the bedsheets. Operation Toga Swap is GO." He stays,
              pacing. (The toga taken, the Gaul's given: `rome.wrongToga`.) The hand that holds the
              toga up, and out, is empty: the people's rig has no toga to put in it (SCENES-13R1).
              Then #10, in the Forum. When the boy comes back with the right one, the delivery below
              plays as it always has, every line but one. His answer to "Late for what?", as it always
              was ("The Senate meets today, in the hall beside Pompey's theater. I have a speech."),
              now also tells the boy where the Senate meets (`rome.knowsSenate`): the Gaul's question.
Wrong tries:  Show the toga to the doorkeeper  -> "Senators are down there. I am up here. We both prefer it."
              Show it to the soothsayer        -> "Not mine. Mine has known soup. That one has a future."
              Show it to the snack-bar keeper  -> "...in my shop, beside my sauce, out, out..."
              Show it to the street boy        -> "Don't let it touch the ground. Don't let it touch
                                                 ME. I'm mostly ground."
              Show him the Gaul's toga again   -> "Put that away. I have seen enough of it for one
                                                 morning. Find the Gaul." (round thirteen)
Solution:     Give him the toga: use it with him, or talk to him and say "Delivery!" (since round
              thirteen, decision 12: "Delivery! One clean bedsheet. Plain white. Like a cloud with a
              job. From the laundry lady."). "A TOGA, boy. A bedsheet covers a man asleep. A toga
              covers a man who matters." "Rome thanks you. I, personally, am far too late." He strides
              off to the Senate and is not seen again.
Gives:        A favor owed. "The laundry lady owes me one tunic."
Teaches:      Handing a thing over: by using it with someone, or by saying so when they talk.
              (Every errand in the act can be finished either way.)
Hints:        Hint button: "I'm carrying a senator's bedsheet. He's the one standing still in a
              hurry, by the temple steps." (Its words unchanged: since round thirteen it speaks for
              the first delivery.) For the second: "I've got the right bedsheet now. The senator's
              still at the temple steps, turning purple. Delivery, take two!" The street boy: "He's
              the big angry one at the foot of the temple steps. Run." And for the second: "You got
              the right toga back? Then run it to the senator. He's still at the temple steps, going
              purple."
Plants/pays:  Pays off the washerwoman's errand. His speech is about drains. "It ends when they agree
              with me." Since round thirteen the place of his speech is the answer to the Gaul (#10).
Notes:        He goes because his figure is already wearing a toga and cannot change it on stage:
              the clean one leaves under his arm. Nothing he says looks ahead to the day's events.
              Once the boy has heard of Caesar (the cut-scene in the street), there is one more thing
              to ask him, until he leaves: "Does Caesar have a kid?" See "The family's faith" below.
              Decision 12: the old line was "Delivery! One clean bedsheet with a purple stripe. From
              the laundry lady."; a senator's toga was plain white (the broad stripe is on his tunic),
              so the line lost the stripe, and the toga's picture and the senator's drawn toga lost
              their purple border. Decision 1: the senator stays on the steps (his move to Caesar's
              door waits, and with it Caesar's house).
```

```
Cut-Scene: Downtown        (the first time he walks into the Forum)        new in round thirteen
```
<!-- ROME-13W -->
He comes down into the square from the far end, where his own temple stands. "The Forum.
It's downtown and church and the bank and a construction site. Ten out of ten. Eleven for
the crane." He looks back down the square: "And way down at the end, that's MY temple. Hi,
door guy! ...He didn't wave. He never waves." And up: "And up on the hill, a gold roof on
fire with sunshine. Rome does NOT do anything halfway." (`rome.forum.arrive.1` to `.3`;
`rome.sawForum`.)
*Plants:* the gold roof on the hill (#11); his temple seen from the far end of the Forum ("My
door guy is a dot."). *Staging:* he arrives at the far end, small under his temple, at the
foot of its steps, and walks a good way down the middle of the square, from where his temple
is "way down at the end" and the crane and the gold roof are both in view; there he turns to
us for the first line, back up the square for the second, and up at the hill for the third.
Coming in from the river, he steps out of the Tuscan street's mouth onto the square.

```
Puzzle #10: Nobody Will Show Him        (Rome · the Forum · the Gaul)        chain A        new in round thirteen
Needs:        #2's turn (he is carrying the Gaul's toga), for the swap. The Gaul can be met before:
              he asks his question, can be answered, thanks the boy, and the swap waits for the toga.
Setup:        At the hoarding round the hole where the senate house stood, in front of its open
              gateway, a very large man in a toga far too short for him walks along the boards and
              back, asking the way of anybody (nobody passes in this stage: the people without lines
              wait for a later one, so he asks the air, and shrugs). "A giant guy in a bedsheet that's
              way too short. His knees are out. Like Dad in my sleeping bag." The boy talks to him from
              beside him, a step nearer us, under the crane. Four ways in ("Hi! Are you lost? I'm lost. We could be lost together."; "Your bedsheet's
              too short."; "Whoa. Are you a VIKING?" "I do not know that word. I am a Gaul. For Rome,
              that is usually enough."; "Which way is... anywhere?"), and he tells the boy, before
              anybody else can: "I am Gaius Iulius Litumarus, of Nemausus in the Province. The
              dictator has made me a senator of Rome." "A senator! Okay. I'm calling you Big Senator.
              It's a compliment." It is his first meeting; he has asked twelve Romans the way to the
              House, and twelve smiled and walked faster. "Someone has put up a notice that no one is
              to show a new senator the way to the House. It is a joke. I am it." He went where the
              House ought to be: "I found a hole full of builders." "So I ask you, since you stopped.
              Where does the Senate meet today?"
Wrong tries:  (the answers to his question are the boy's choices)
              "In the senate house!"         -> He turns to the site and points at the hole. "There is the
                                                senate house. It is a hole with men in it." "...Oh.
                                                That's a VERY open-plan senate house." (Again: "It is
                                                still a hole. I have looked again. Holes are like that.")
              "Up on the Capitol? With the gold roof?" -> "I have been up. There are geese." "They did
                                                not show me the way either. They showed me the way
                                                down." (Once the boy has been up: "Up on the Capitol?
                                                Past the attack chickens?" "You have met them. Then you
                                                know why I came down again.")
              "At Caesar's house? He's the boss, right?" -> "I have been there. Nine hundred senators
                                                and one porter." "...That's a LONG line."
              "I don't know. Honestly. I'm new here." -> "Then you are a true Roman. Thank you." He bows.
              Hold out the Gaul's toga first  -> (it opens his talk, where "Swap?" is on offer while the
                                                boy carries it) "First the Senate. Then my knees. Where
                                                does the Senate meet, child?"
              The coin, the quarter, the phone, the gum, the breakfast, the incense, the lamp, the
              senator's toga before the turn -> a line each, in his voice ("A small dark mirror. It shows
                                                a large man in a short toga. I knew.").
Solution:     "In Pompey's hall, by his theater.", on offer once the boy has heard it
              (`rome.knowsSenate`): from the senator (his old line, "The Senate meets today, in the
              hall beside Pompey's theater. I have a speech."), or from Walnut. "Pompey's theater. The
              great stone one, on the plain, with the temple on top of its seats?" If the boy has
              looked at it from the Capitol (`rome.sawTheater`): "Yes! I saw it from the top of the
              hill!" "Then I have my way from a boy who has seen it with his own eyes. That is more
              than the Senate gave me." If not: "That's the one. I think. The senator told me. He's
              giving a speech there. About drains." "A man does not invent a speech about drains. I
              believe you." Then: "Pompey's hall. Of course. They cannot meet in a hole. Even Rome
              cannot meet in a hole." "Someone has shown a new senator the way. The joke is spoiled,
              and I thank you for spoiling it." (`rome.gaulAnswered`.) He will not go yet: "A new man
              does not arrive first. It looks keen." "And I would rather not cross Rome with my knees
              out." Then the togas, once the boy has the Gaul's toga and the answer is given, in either
              order: "Big Senator! That toga's my senator's. He's got yours. Well, I've got yours.
              Swap?" He looks down at his shins: "...I had decided Roman togas were made to be
              ridiculous." The boy holds out the enormous toga and he takes it; he goes into the
              hoarding's gateway and behind its near boards, where not a hair of him shows; a while;
              and he comes out in his own, falling properly to his ankles, and holds out the senator's,
              folded, which the boy takes: "There. Now I look like a senator. All that is left is to
              be one." "Operation Toga Swap: complete. One bedsheet, senator-sized. Back to my
              senator." And his going: "If anyone asks, a Roman showed me the way." "I'm not a Roman."
              "Then nobody will be blamed." He walks off up the square, between the site and the
              colonnade of Paullus, toward the plain, and is gone where the square leaves the picture;
              he is not in the Forum again.
Gives:        The senator's own toga, in place of the Gaul's (`rome.swapped`). Then #2's delivery.
Teaches:      Talk is a tool: something heard at one end of Rome answers a question at the other.
Hints:        Hint button: "The senator's toga is on a lost Gaul in the Forum. He wants to know where
              the Senate meets. My senator would know." (One line that helps whether he has heard it
              yet or not.) The street boy: "A big Gaul in a little toga? Tell him where they meet:
              Pompey's hall, by the theater. Their House is a hole." (Hearing it from Walnut puts the
              answer on offer too.)
Plants/pays:  Pays the senator's old line about Pompey's theater, and his speech about drains. Pays
              the theater seen from the Capitol ("Biggest bleachers EVER."). Pays the senator's "He
              will be in the Forum, lost. They are always lost."
Notes:        Never mocked: the joke is Rome's, and he is the one who tells it. He tells the city's
              song about Gauls in his own words ("Gauls who took off their trousers to put on the
              broad stripe. I have heard it nine times. It does not improve."), and the verses are
              never quoted. The laughs are the song ("Ten times now. I caught myself humming it this
              morning. Tell no one.") and his mustache ("Ten out of ten on the mustache." "Every man
              of rank in my country wears one. Every man in Rome shaves, and stares."). Nothing he
              says looks ahead to what happens in that hall today: he is going to an ordinary meeting.
              His talk is `gaulTree`; the scene's hooks: `point`, `bow`, `swap` (the togas change
              hands there, and `rome.swapped`), `leave`. The order is free: met before the turn, he
              asks, is answered and thanks the boy, and the swap waits for the toga; met with the
              Gaul's toga before the answer, he wants the answer first.
```

```
Puzzle #3: Collect The Tunic        (Rome · the street · the washerwoman, or the low line)        chain A
Needs:        #2
Setup:        The tunic still hangs on the low line. She keeps her word: "Toga first, then tunic. I
              have run a laundry for twenty years on 'first' and 'then'."
Wrong tries:  Ask before the toga is delivered -> the line above.
Solution:     Talk to her, or reach for the tunic. "One bedsheet, delivered! He said Rome thanks
              you. He was too late to say it himself." "That sounds like him. Here. My sister's boy
              has outgrown it. Bring it back clean."
Gives:        The small tunic. The painted tunic leaves the line.
Teaches:      Go back to whoever sent you.
Hints:        Hint button: "Bedsheet delivered. The laundry lady owes me one tunic. Time to collect."
              The Son says the same when the senator leaves.
Notes:        "A real Roman tunic. It's a dress with a belt. Nobody tell my school."
```

```
Puzzle #4: Take The Breakfast        (Rome · the street · the snack bar)        chain B
Needs:        nothing
Setup:        The keeper sends the old soothsayer bread and a sausage every morning, and has for
              eleven years. Since round thirteen: this morning his boy Titus took it at first light
              and has not come back. It is the Ides, and every Ides the boy runs after the white ewe
              that goes up to Jupiter, every single Ides.
Wrong tries:  Pay with the quarter      -> "Who is this? I know every consul's nose. That is not a
                                          consul." "That's George. Back home, EVERYBODY knows that
                                          nose." (PASS-17R, round seventeen) "...you pay me later,
                                          everyone pays me later."
              Pay with the fountain coin -> "THAT nose I know, that is Caesar, struck this year..."
                                          "I can't spend it, though. It's a borrowed wish."
              Bring the breakfast back   -> "No, no, UP the street, the old one with the chickens..."
Solution:     Talk to him. He feeds the boy before anything else ("you are too thin, everybody is
              too thin, here, eat, eat"), and then (CHANGED in round thirteen: the same four ids,
              re-worded, and one new line, the ewe): "Never mind, you have legs, fast legs, good, I
              need legs, I have lost a boy, my Titus, and a breakfast with him." "Bread and a sausage,
              every morning, eleven years, the old soothsayer's, my boy took it at first light and
              never came back." "It is the Ides, every Ides the white ewe goes up to Jupiter and my
              boy goes after her, every single Ides." "Go up the hill, bring me down my boy, and the
              breakfast, the old one will be fainting, he will say he foresaw it." "Operation Sausage
              Rescue. Find the kid, find the sausage. I won't eat it. I'll just THINK about eating it."
Gives:        A snack: "Step one: DONE. Nine out of ten." And where the breakfast is
              (`rome.knowsBoy`): since round thirteen he no longer hands it over. Titus does, on the
              Capitol (#11).
Teaches:      The same lesson as #1 from the other end: this errand finds him.
Hints:        Hint button: "Something for the god: the chicken man has incense. And no breakfast. The
              snack bar has breakfast." (Its words unchanged: the snack bar is still where to ask, and
              since round thirteen the beat ends when the keeper has said where his boy is.) The
              soothsayer: "My bread and sausage come up from the cookshop by the fountain. Not this
              morning." The street boy says both halves (the second re-worded in round thirteen: "The
              sausage man sends it up every morning. Today his boy took it at first light, and never
              came back.").
Plants/pays:  Pays off "Step one: snacks". Plants no tomatoes: "It only needs ketchup." "What is a
              tomato?" "...No tomatoes. Dad's been saving those little packets for years. He KNEW."
              Plants Titus, and the ewe (#11).
Notes:        The errand as it was before round thirteen: "Never mind, you have legs, fast legs, take
              this to the old soothsayer on the temple steps." "Bread and a sausage, every morning,
              eleven years, my boy has not come, I cannot leave the pot." "Tell him he owes me for all
              eleven, he will say he foresaw it, he always foresaw it." "Operation Sausage Express. I
              won't eat it. I'll just THINK about eating it. That's allowed." (Walnut's old second
              half: "The sausage man sends his breakfast up every morning. Today it's still on the
              counter.")
              If the boy has met Titus first: "I found him already! He's sitting on a statue up the
              hill. With your breakfast. And a LOT of geese." "Geese! Every Ides the ewe, and now
              geese, go back up, bring him down, the old one will be fainting." If he walks in
              carrying the breakfast: "That cloth! That is my cloth, that is the old one's breakfast,
              where is my boy, where is my Titus?" "On his way home! He was stuck on a statue. There
              were geese. I did a stomp. It's a long story." "Geese, every Ides something, take it up
              the street to the old one, quick, before it is a lunch." And once Titus is home: "My boy
              is home. He says your shoes frightened Juno's geese. NOTHING frightens those geese. Have
              a sausage." "Thank you! I won't even ask about the ketchup. I've grown as a person."
```

```
Cut-Scene: Would Climb        (the first time he comes up the hill to the Capitol)        new in round thirteen
```
<!-- ROME-13W -->
"The temple on the hill! Ten out of ten. Would climb. DID climb." "And you can see the WHOLE
city from up here. It's like a map that's on." "Also there's a kid sitting on top of a
statue. Surrounded by geese. That's a whole situation." (`rome.capitol.arrive.1` to `.3`;
`rome.sawCapitol`.) He comes in at the gate, which is behind us, and takes a step up into the
precinct; he looks up the paving at the temple for the first line, over the parapet at the
city for the second, and up at the kid on his base, with a honk from the geese, for the
third. (A game saved before round thirteen, with the breakfast had from the keeper, finds
nobody on the base and the geese in their pen, and the third line is left out.)
*Plants:* Pompey's theater, out on the plain, in the view (#10); the kid (#11).

```
Puzzle #11: Juno's Geese        (Rome · the Capitol · the keeper's boy, the geese, the goose-keeper)        chain B        new in round thirteen
Needs:        The Capitol open (`rome.knowsBC`). For the hint, #4: the keeper has said where his boy
              is (`rome.knowsBoy`); a boy who comes up the hill first hears it from Titus himself.
Setup:        On top of the middle statue base among the kings sits a boy hugging a bundle, and round
              the base's foot stand the sacred geese. "A kid sitting on top of a statue base, hugging
              a bundle. He's pretending he meant to be up there." Titus, the keeper's boy: "Stuck? Me?
              I'm SITTING, I like sitting, I can see the whole city from up here, you can't, you're
              down there." He has been sitting since first light. On purpose. Mostly on purpose. "This
              is old Arruns's breakfast, the soothsayer's, I was taking it to him at first light, and
              then the ewe went by." "So I went after her, I always go after her, every Ides, and then
              the geese came, and now I'm sitting. On purpose." Whenever he puts a foot down, every
              goose stretches its neck out low and hisses (asked about the geese, he shows the boy,
              and draws his knees up to his chin). Behind his pen, the goose-keeper will not move
              them: "Sacred birds. I feed them. I do not argue with them." The boy talks to Titus
              from before the base, by its right corner, looking up at him, and to the goose-keeper
              from beside him, behind the pen.
Wrong tries:  Call the geese         -> "Here, goosey goosey... They hissed at me. In stereo."
              Shoo them              -> "SHOO. ...They didn't shoo. They're not shooers." (The geese are one
                                        thing to use, "Shoo sacred geese": calling and shooing come in turn,
                                        and at each, as at everything tried on them, every goose
                                        stretches its neck out low and hisses.)
              The gum                -> "No gum for sacred geese. They'd never get it off their beaks."
              The quarter            -> "They don't want a bird. They ARE birds."
              The coin               -> "Bribing geese. That's a new low. Even for me."
              The phone              -> "They hissed at the phone. That's more than it's done all day."
              The toga               -> "Throw a senator's toga over sacred geese? They'd honk under it
                                        forever."
              The Gaul's toga        -> "Throw a whole Gaul's toga over them? I'd lose the geese, AND the
                                        toga. And probably me."
              The lamp, the tunic    -> a line each ("Not Felix's lamp. If anything happens to it,
                                        Phyllis will know. From across the river.")
              Ask Titus to jump      -> "Over THEM? They bite like Father's creditors." Again: "You'd
                                        catch me and they'd catch you. And then where would we be?
                                        Down THERE. With THEM."
              Ask the goose-keeper to move them -> "I have fed them thirty years. I have never once won
                                        an argument with them."
Solution:     Ask the goose-keeper how geese saved a city (Titus: "Ask old Anser, he feeds them, he
              talks about them all day. He's never once moved them."). He tells it as he would tell
              it, long ago and with no year: "Long ago, the Gauls took this city. All of it, but this
              hill." "One night they climbed the rock below that wall. So quietly that not even the
              dogs woke." "But Juno's geese woke. They cried out, and beat their wings, and woke
              Manlius." "Manlius ran to the edge and knocked the first Gaul down, and the rest went
              down faster than they came up." "So the geese are Juno's, and the Republic feeds them,
              and nobody argues with them." "They cannot abide anything strange. They shout at it, and
              then they run." (`rome.knowsGeese`.) "Anything STRANGE. ...Huh. I'm thinking. I've got
              my thinking face on." Then, from his talk ("Mister Goose? You might want to hold on to
              your basket.") or with a click on the geese once the tale is told, the boy walks to the
              foot of the base, faces it: "Anything strange? I'm the strangest thing in Rome. Watch my
              feet." He stomps; his sneakers flash red, twice (once, softly, for less motion); the
              geese shriek, flap and run for their pen, the nearest to him first, through the gap the
              open gate leaves in its side, and are in (for less motion they walk in, briskly). A
              honk from the pen. Titus hops down off his base, the bundle clutched to him: "I wasn't
              scared. I was SITTING." He comes over to the boy and holds the breakfast out by its knot:
              "Take it down to old Arruns, I'm going home before Father sends the geese after me." The
              boy takes it: "Operation Sausage Rescue: complete. One kid, one breakfast. Zero geese."
              "Your shoes are the best thing on this hill, and I've seen the gold roof!" And he runs
              off down the hill, out at the gate behind us, and is gone home. The goose-keeper: "That
              is the most noise they have made since the Gauls." From then on the geese are in their
              pen, eating as if nothing had happened ("Every goose back in the pen, eating like nothing
              happened. Professionals."; "I'm not going near them. We had a moment. It's over."), and
              the base is empty.
Gives:        The soothsayer's breakfast (`rome.hasBreakfast`; the geese in their pen,
              `rome.geeseGone`).
Teaches:      Listen to the old man's story: it is the instructions.
Hints:        Hint button: "The snack guy's boy is stuck up the hill with the breakfast. Geese.
              Somebody up there knows about geese." The street boy: "The Capitol geese? My uncle says
              they woke the hill when the Gauls came. They scream at anything they've never seen."
              Titus: "Ask old Anser."
Plants/pays:  Pays Walnut's "Stomp when you go. So I can watch.", and the shoes that light up when he
              stomps (the street). Pays the keeper's errand (#4) and the ewe, and the gold roof seen
              from the Forum. The keeper, the next time: "My boy is home. He says your shoes frightened
              Juno's geese."
Notes:        The geese hiss, and nobody is hurt: it is a standoff, and funny. The Ides ewe has gone up
              and been offered before the boy comes, and nobody says how: the altar is out, "Just
              smoke." The tale is Rome's own history, part legend, told as the goose-keeper tells it
              (Livy 5.47); no year is said. His other talk: the dogs that guard the hill at night
              ("Between you and me, the dogs sleep. The geese never do."), his name ("Anser means
              goose." "It was my grandfather's name before it was my job. Nobody believes it." "I
              believe it! A goose guy called Goose. Mister Goose! You go straight to the top of my
              collection.": PASS-17R, round seventeen), and Juno's other
              temple on the hill's other summit, Moneta, where they make the money ("Moneta.
              MONEY-ta. ...I just figured out the word money."). The second time, he tells the tale
              gladly ("...You were listening. Nobody listens. Thirty years, and nobody listens."); the
              third, "Long ago..." "I'm going to stop asking you that. For both of us." After the
              stomp: "Sorry about the noise." "Do not be sorry. Thirty years I have told that story.
              Today somebody USED it." The talks are `titusTree` (hook `feet`) and `anserTree` (hooks
              `shake` and `stomp`: the stomp is one script, from his talk or from the geese). Whose
              boy and whose breakfast are known by the hand-over at the latest, so a boy who stomps
              before he has said a word to Titus, or before the keeper has sent him, is not stuck.
              The goose-keeper stays behind his pen, and does not walk out among the geese round the
              base (DESIGN.md, section 14).
```

```
Puzzle #5: Feed The Soothsayer        (Rome · the steps · the soothsayer)        chain B
Needs:        #11 (since round thirteen the breakfast comes from Titus; before, from #4)
Changed:      Round thirteen: when the breakfast has come down the hill, the boy's first line as he
              hands it over is "Breakfast! It's been up a hill and past some geese.", in place of
              "Breakfast! From the snack guy. He says you owe him for eleven years." (which stays for
              a breakfast from the keeper, in a game saved before). The rest as it was.
Setup:        An old soothsayer sits on the steps beside a cage of sacred chickens. He has incense
              for Saturn that should have gone in at dawn, and bad knees: "There are fourteen steps
              between it and him. My knees have foreseen every one." The boy offers to carry it.
              "Not today. The birds will not feed, and I have no breakfast to tempt them. I send the
              god nothing."
Wrong tries:  Call the chickens              -> "They can tell I don't have snacks. Chickens always know."
                                                And, the first time: they are all facing the temple
                                                doors (see "The chickens, and the years", below).
              Feed the breakfast to the birds -> "If I feed it to his chickens, he'll foresee me doing it."
              Take the breakfast to the doorkeeper -> "I do not eat at the door. ...Is that the sausage
                                                from the street with the fountain?" "It's the chicken
                                                man's." "Then it is the chicken man's."
Solution:     Give him his breakfast: use it with him, or say "Breakfast!" when they talk. "I foresaw
              this sausage at dawn. It is the only thing I have foreseen all year that I wanted." He
              crumbles bread for the birds. They feed. "A good omen. For somebody. It may even be
              you. Take this incense in to the god, boy. Fourteen steps. My knees send their regards."
Gives:        The incense box.
Teaches:      An errand can have a reason behind the reason: he is not being stubborn, he is waiting
              for an omen, and the omen eats bread.
Hints:        Hint button: "The chicken man's breakfast is in my backpack. It's getting cold. So is
              he." The street boy: "That's old Gloom's breakfast going cold in your bag."
Plants/pays:  Pays off the keeper's errand, and the fourteen steps the Son counted "on the way down.
              Upside down."
Notes:        The first time they speak: "Beware the Ides of March." "Which one is Ides?" "Today."
              "Then it's a bit late to be-ware." "I said it in February, too. Nobody listened then,
              either." His gloom is the game's only nod to the day, and the Son does not understand
              it: "Okay. Bye! Happy Ides!" "It is not that kind of day."
              Asked about the birds before they have fed: "Today they will not touch a grain." "The
              worst omen there is, and on the Ides. I sell omens, boy. This one I could not give away."
              They will not touch their grain, and they eat the cookshop's bread: whatever they know,
              they are still chickens.
```

```
Puzzle #6: Three Out Of Three        (Rome · the steps · the doorkeeper)        the gate of chains A and B
Needs:        #3 and #5
Setup:        The doors stand wide open and the doorkeeper stands in them. Asked, he says exactly
              what he lets in: "Boys go in. The boys who serve at the rites. A boy. In a clean tunic.
              Carrying something for the god. You are a boy. That is one out of three." "He does
              scores! Out of THREE, though. Weird system."
Wrong tries:  With neither      -> "One out of three. I am not a difficult man. I am an exact one."
              The tunic only    -> "A clean tunic. Good. And for the god you bring two empty hands.
                                   Two out of three." "My score went UP. I'm improving!"
              The incense only  -> "Incense for the god. Good. Carried by a boy dressed as I do not
                                   know what. Two out of three." "It's a hoodie. It's from the future.
                                   It was on sale."
              The coin          -> "One coin. For the treasury. It has others."
              The quarter       -> "That is not a coin. I do not know what it is. Put it away before I
                                   have to find out."
              The dead phone    -> "A small black door. It is shut. I approve."
Solution:     Try the doors, or talk to him, carrying both. "Tunic: ON. It goes over the hoodie. And
              the backpack. I'm a lumpy Roman." "...Three out of three." "YES." "The hair." "It doesn't
              go down. I've tried. Mom's tried. Gravity's tried." "...Go in. Walk. Touch nothing. The
              clerk is counting."
Gives:        The inside of the temple, for good. After this he is waved through.
Teaches:      This is the puzzle of the act, stated in the first minute by the man in the way.
Hints:        Hint button: "Clean tunic: got it. Something for the god: got it. Time to show the door
              guy my score." The street boy: "Tunic. Incense. So GO. Before Doorpost thinks of a
              fourth rule."
Plants/pays:  Pays off both errands at once. Everybody scores things in this act; he is the only
              one who does it out of ten.
Notes:        A player who has run both errands before ever asking gets the rule and the pass in
              one go. One who asks with one errand done is scored on what he is carrying.
              THE TUNIC IS NOT DRAWN. The Son's figure cannot change clothes yet, so he pulls it on at
              the door, where he is small, and pulls it off again the moment he is inside ("Tunic:
              OFF. It itches like a sweater made of hay. Two out of ten. Romans are tough."). If a
              figure of him in a tunic is ever drawn, show it while `rome.inside` is true and he is
              in the temple, and cut that line.
```

```
Puzzle #7: Borrow A Wish        (Rome · the street · the fountain)        chain C
Needs:        nothing
Setup:        A fountain with coins glinting under the water. "People throw coins in the water here.
              On PURPOSE. I love this place."
Wrong tries:  Take a second one             -> "One wish is borrowing. Two is a crime spree."
              Pay it back with the quarter  -> "Somebody digs that up in two thousand years and has SO
                                               many questions."
              Throw it back                 -> "I haven't even used the wish yet. I'm saving it for
                                               something big. Or small."
Solution:     Reach in. "Operation Borrow-A-Wish is GO. Splish." "Brand new, and SO shiny. I can see
              my face in it, next to the serious man. He's not happy about it."
              Then, after the street boy has had his say (below), his first hard look at it: "It says
              CAESAR on it. So that's the nose the snack guy yells about. It's the Caesar coin!" "Like
              in the story! They ask Jesus about taxes, and He says, show me a coin. Whose picture is
              on it?" "Caesar's. So Caesar gets his coin. And God gets what's God's. Which is
              everything. Me included." "But Jesus is all grown up in that story. So this isn't that
              Caesar. Not yet."
Gives:        The silver coin.
Teaches:      Nothing yet, and that is the point: it is a shiny thing picked up because it was there.
              What it is for comes later (#8).
Hints:        Hint button (only once he is inside without it): "That fountain is full of other
              people's wishes. I only need to borrow one." The street boy, asked how to put light on
              a wall: "Shiniest things on this street are the new silver ones in the fountain. They
              flash like fish."
Plants/pays:  Plants shiny, twice. He reads the name on it himself, and the keeper, shown it, says
              when it was struck ("this year"): the Son never learns why that matters. Big Sister
              does, in Act Four, where the same story is told again with the verse (Mom's).
              Pays off the keeper's cry: "the new has Caesar's nose on it".
Notes:        The street boy sees him do it: "That's somebody's wish, you know." "I'm only borrowing
              it. I'll pay it back with interest. Interest is extra wishes."
              Round thirteen (ROME-13W): Walnut goes on, and says whose: "It's Phyllis's. The garland
              woman, by Castor's temple. She threw it in at first light, for her boy. He's going to
              Corinth." "Then I'll ask her. You can borrow a wish. You can't throw somebody's wish
              away." (`rome.knowsWish`: #12.) A game saved with the coin before this hears it from
              Walnut the next time he walks into the street. The four kept lines are as they were.
```

```
Puzzle #8: Tiny Sun        (Rome · the temple · the sunlight on the floor)        chain C
Needs:        #6 and #7
Setup:        The single dark room. A god at the far end with his feet tied in wool; chests of the
              Roman People's money down both walls; a clerk counting it by lamplight; one hard patch
              of morning sun on the floor from the doors. And on the left wall, in shadow, the hum.
              "It's doing the hum again. Hi, door." "You're shut. AND invisible. But I can hear you.
              You're terrible at hide-and-seek."
Wrong tries:  Touch the place that hums   -> he works it out: "In the big pointy place I shined my
                                             flashlight at the hum, and POP: door." The flashlight
                                             got left behind. "Phone light!" "Zero percent. It can't
                                             even be sad about it." "So the door likes light, and I'm
                                             all out. I need the kind you don't have to charge."
              Stand in the sunlight       -> "With something shiny I could bounce this anywhere. I do
                                             it with a spoon at breakfast." "Mom has asked me to
                                             stop. Twice a week."
              The coin, held up to the hum -> "It's dark over here. A coin's only shiny where there's
                                             sun to be shiny WITH."
              The phone, in the sun       -> "The screen's cracked. I get a hundred tiny lights going
                                             a hundred ways. Pretty. Useless."
              The gum, in the sun         -> "Paper wrappers. No foil. Whoever made this gum did not
                                             plan for time travel."
              The quarter, in the sun     -> "This quarter's been through the wash and two vending
                                             machines. No shine left. I need a NEW coin."
Solution:     Use the coin with the sunlight on the floor. "Operation Tiny Sun. Sun, meet coin. Coin,
              meet wall." The first try goes down the wrong wall and across the clerk: "...five
              hundred and six, five hundred and sev... AGH. My eye." "Sorry! Wrong wall!" "What was
              that light?" "The sun. It does that sometimes. It's a known sun thing." "...One. Two.
              Three." The second try, while he counts: "Okay. Slowly. Tip... tip... a little left..."
              The spot lands on the place that hums. "POP! A door! A tiny one. It's exactly the size
              of the coin." "Little light, little door. That's only fair." He goes and looks through:
              "There's sky in there. Blue. Really far down. ...Why is the sky DOWN?"
Gives:        A door in time, the size of a coin. It stays.
Teaches:      The rule of the doors, in his words: the door likes light; little light, little door.
              (Dad learns the other half in Egypt: a whole sun, a whole door.)
Hints:        Hint button: "The door likes light. There's sun on the temple floor and a shiny coin in
              my backpack. Bounce it!" The street boy: "Easy. Something shiny, in the sun. I do it to
              the sausage man with a pot lid. He hates it."
Plants/pays:  Pays off the coin, and the flashlight from before the act. Plants "Why is the sky DOWN?":
              the other side of this door is high over a desert.
Notes:        The clerk must not see, and does not: he is the comedy of it and never the obstacle.
              The three wrong tries in the sun are there so that every shiny thing he owns has been
              thought of and has an answer. The light is drawn live: the spot (`#glint`), a faint beam
              from the coin (`#ray`), and the game's own wormhole at a radius of 11 (`#hole`, in `#door`),
              out of sight until this moment. To touch the place, and to look through the door, he
              stands at the far end of the floor's edge, where his head is level with it and the words
              over his head do not lie on top of it.
              Round thirteen: unchanged. Phyllis's lamp, if he is carrying it, is tried in here too
              and is not the answer: "It's clay. Clay doesn't shine. The coin's the shiny one. The
              lamp's the precious one."
```

```
Cut-Scene: Like Daniel        (the first time he comes off the stone bridge)        new in round thirteen
```
<!-- ROME-13W -->
He comes off the bridge, takes a step onto the lane, and stops: "Over the river: boats, a
girl with a whole lot of hens, and up in that window, an old man with his eyes shut." He
looks up at the window: "He's praying. With his window open. Like Daniel." And to us: "I'll
wait till he's done. ...I'm getting good at waiting." (`rome.tiber.arrive.1` to `.3`;
`rome.sawTiber`.) Every way through the act passes it, since Felix is there (#12).

*The wait.* The old man stays at his window, at his prayer, until the boy has waited for
him. The first click on him there ("Wait for old man"), on his house or his door ("Knock
at": "Knock? Not while he's praying. You don't knock on somebody's praying."), on his window
("Wait under") or on the bench ("Sit on": "I'll sit. Sitting is the main part of waiting.")
is the wait: the boy goes to the near end of the bench and stands facing the house (he
cannot sit: the people's rig has no seated drawing of him); a few seconds pass, the old man
lifting his head at the window, his lips moving; to us, "Waiting. I'm doing it. Look at me
doing it."; the old man steps back from the window and is gone; a moment; he comes out of his
door with his scroll, the boy steps aside out of his way, and he walks along the front of
the bench and sits down on it; the boy comes back to its near end, and the talk begins
(`rome.eleazarDown`). *If the boy does not wait*: once he has seen the old man at his prayer,
whenever he leaves by the bridge the old man finishes while he is gone, and is on his bench
when he comes back (a game saved and loaded during that first visit still has him at his
window). <!-- MAP-15D --> Since round fifteen the same when he leaves by the map: it is the
scene's `leaving` that sets it, however he goes.
What follows is under "The family's faith" below: it gives and needs nothing, and
the act does not wait for it.

```
Puzzle #12: Interest Is Extra Wishes        (Rome · the Forum, and across the Tiber · Phyllis, and Felix)        chain C        new in round thirteen
Needs:        #7 (the coin), and Walnut's word whose wish it was (`rome.knowsWish`). Needed for #9.
Setup:        When the boy borrows the coin, Walnut says (as always) "That's somebody's wish, you
              know.", and now whose: Phyllis's, the garland woman's by Castor's temple, thrown in at
              first light for her boy, who is going to Corinth. In the Forum, at the foot of Castor's
              temple, Phyllis sits on her low stool among her baskets, the little lamp wrapped in a
              cloth in her lap; the boy talks to her from a step out on the square, on her right:
              "Violets! Laurel for your doorpost! Myrtle for
              your sweetheart! A garland for Anna Perenna!" It is Anna Perenna's feast: "Half the city
              is going out to picnic on the grass by the river." "And every one of them wants a
              garland, NOW. The busiest morning of my spring. I can't leave my baskets a moment." (She
              gets up then to hang a garland on her pole, and sits again.) Her
              one son, Felix, loads the barges across the river, below the stone bridge, and his name
              is down for Corinth: "The dictator is building it again, mostly for freedmen. Like me."
              "A city that has lain empty a hundred years. Imagine. Houses with nobody's grandmother
              in them yet." Asked, with the coin, knowing whose it was ("Walnut says this was your
              wish. In the fountain. I borrowed it. I'm asking now."): "...My wish. Yes. I threw it in
              at first light, for my boy." "The first new silver I have held in years. The dictator's
              own head on it. I thought it would carry a wish far." "I wished to give Felix this before
              he sails. A little lamp, to light his new house in Corinth." "And to hear him say he will
              come and say goodbye. But he can't leave his barge, and I can't leave my baskets."
Wrong tries:  Give her back the coin       -> "A wish once thrown is not mine to take back. But it was
                                              for my boy."
              Pay her with the quarter     -> "Or I could pay you for it! With a quarter. It's got a
                                              bird on it." "A bird? For a wish? Child."
              "Can I think about it?"      -> "Think, then. But Corinth will not wait for you to finish."
              Hold the lamp up to the hum  -> "It's not lit. And it's not mine. It's a goodbye present."
              Toss the coin before she has said he may -> "Wait. This is Phyllis's wish. I'm not
                                              throwing somebody's wish through a door without asking."
                                              (#9; nothing happens)
              The lamp, shown to anybody else -> a line each (the keeper: "A lamp, a good little lamp,
                                              for Felix, for Corinth, everybody knows, everybody eats
                                              here, I hear everything").
Solution:     "I could take the lamp to him! I'm great at errands. This is, like, my fourth today."
              "Would you? He works the barges across the river. Down the Tuscan street, and over the
              stone bridge." "Tell him his mother says come before he sails. He will know the rest."
              She unwraps the lamp and holds it out in both hands, and the boy takes it: "Operation
              Lamp Delivery is GO. I'll carry it like an egg." (The lamp: `rome.hasLamp`; in her hands
              now, a half-made garland.) Across the Tiber, Felix carries bales between the landing
              and the barge's side, a bale on his shoulder; the boy talks to him from a step east of
              him on the landing. "Special delivery! From your mom. A lamp, for your new house in
              Corinth." He turns to the pile and sets his bale down.
              "...From her? She can't leave her baskets. She sent you?" "She threw a wish in the
              fountain for you, too. A new silver one. I sort of borrowed it." "She threw a coin in a
              fountain? For ME?" "...She never throws anything. She keeps string." "She wants to hear
              you say you'll come. Before you go." "So? Will you come and say goodbye?" The boy holds
              out the lamp, and Felix takes it: "Tell her I'll
              come over the bridge at the ninth hour, before the barge goes down." "And tell her I'll
              light it in Corinth. The first night. In the first window." (`rome.felixWord`.) "Operation
              Lamp Delivery: delivered. And I'm taking a promise back. That's a two-way errand." After
              the talk he takes up his bale again and goes back to work. Back in the Forum: "He'll come
              at the ninth hour. And he'll light it in Corinth." "...The ninth hour." "Then the wish is
              answered, and it was a good one." "Keep the coin, child. It has done its work, and it was
              borrowed honestly." (`rome.wishGranted`.) She gives her leave with no gesture: a short
              pause (the people's rig has neither a hand closing over a coin nor a nod for her where
              she sits: SCENES-13R1). "Borrowed. Paid back. With interest. I TOLD Walnut interest is
              extra wishes."
Gives:        Her leave to send the coin through the door (#9). The lamp goes to Felix.
Teaches:      What the act has said all along: he is borrowing. Here he asks first, and pays it back,
              "with interest".
Hints:        Hint button: "That's Phyllis's wish. I'm not throwing it through a door without asking.
              She's in the Forum, with the violets." Then: "Phyllis's lamp is for her boy, Felix. He
              loads barges across the river." Then: "Felix said yes. Go tell his mom!" The street boy,
              asked what to do with a door the size of a coin: "Put a coin through it. But that one's
              Phyllis's wish. Ask her first: Castor's temple, in the Forum, the violets."; then "First
              the lamp. Felix works the barges over the river: down the Tuscan street, over the stone
              bridge. Big. Sunburnt."; then "Felix said yes? Then tell Phyllis before you throw
              anything. A wish isn't done till the one who wished it hears."
Plants/pays:  Pays the act's own "I'll pay it back with interest. Interest is extra wishes." (#7). Plants
              the coin's last journey (Act Four) with a mother's leave. Corinth: "Corinth. That rings
              a bell. A big one. ...It'll come to me." It comes to him across the river (the faith
              thread, below).
Notes:        The laugh in her talk: "Myrtle for my sweetheart? I don't have a sweetheart. I don't even
              have a DOG." "No dog and no sweetheart. Then violets for your mother. Every boy has one
              of those." "...Mom would like that. She's a long way away. A REALLY long way." In his:
              string ("Every bit that ever came into our house. In a jar. Since before I was born." "My
              mom keeps rubber bands. On the doorknob. It's a BALL now."). Felix's other talk: the
              barge ("A table doesn't go down to Ostia and back."), Ostia ("The big ships can't come up
              the river. They wait off the shore."), Corinth ("It's lain empty a hundred years, and the
              dictator's building it again." "A house of my own, in a city with a sea on each side."),
              his mother ("So I wave at the Forum. She can't see me. I wave anyway."). When the
              colonists sailed is not known, and nobody names a day; nobody says what the city is like
              at the ninth hour today. The talks are `phyllisTree` (hooks `stand`, `lamp`, `grant`) and
              `felixTree` (hooks `setDown`, `lamp`, `aside`).
```

```
Puzzle #9: Heads, Tails, Edge        (Rome · the temple · the coin-sized door)        THE GATE
Needs:        #8; and, since round thirteen, #12 (Phyllis's leave: `rome.wishGranted`)
Setup:        A door he cannot fit through. "My eye fits. The rest of me has to wait."
Wrong tries:  Go through it        -> "I'm not jumping in there again without a snack. That's a rule I
                                      made up just now and I stand by it." "Also I'm bigger than a
                                      coin. That's the other rule. Physics made that one up."
              Send the quarter     -> "Not the quarter. George is the only other American in Rome. We
                                      stick together."
              Send the phone       -> "It won't fit. Also it's dead. A dead phone is not the message I
                                      want to send Dad."
              Toss it before Phyllis has said he may -> "Wait. This is Phyllis's wish. I'm not throwing
                                      somebody's wish through a door without asking." Nothing happens.
                                      (round thirteen)
Solution:     Use the coin with the door. "Heads, I find Dad. Tails, Dad finds me. Edge, we get a dog."
              "... It didn't come back down. Does that count as edge? Do we get the dog?"
Gives:        The end of the act: "Meanwhile, about two thousand years later", and the living room.
Teaches:      What goes into a door in one year comes out of a door in another. He does not learn
              it. The player does, in Act Four, when it hits an old man's hat.
Hints:        Hint button: "The humming door ate me. Maybe it eats money too. For science." The
              street boy: "A door the size of a coin? Then put a coin through it. What else fits?"
Plants/pays:  The coin lands in Nevada in the present, new, with Caesar on it: half of what Big
              Sister needs. This is the first time one half of the family helps the other.
              "Edge, we get a dog" has a dog to mean now: the one asleep on the Forum.
Notes:        The toss, the card and the change of act are the old scene's own code, kept as it was.
              Since round thirteen it waits for Phyllis's leave (decision 7); with it, everything here
              is as it was, the kept lines too.
```

Also in the scenes, for character and nothing else. **On the steps:** the temple front
("Giant stripy pillars... Would climb."), the steps themselves, the Forum ("It's recess
for grown-ups"), the altar ("A stone barbecue wearing a flower necklace"), a bronze
tripod ("A giant bronze cake stand. No cake."), the stone carved S P Q R ("No vowels.
You can't even sneeze that."), pigeons, and three things the painter added: the notice
board on the temple's base ("Rome has terms and conditions."), a handcart of sacks at a
low door ("The treasury has a drive-through."), and a dog asleep in the shade ("I ask
for one every birthday. Dad says we'll see. We never see."). **In the street:** the
washing lines, the laundry basket, the stepping stones (whose second look is at the road
itself: see below), a cat ("Cats were already like this") and the songbird it is watching ("The cat over there is a big fan. A BIG fan."),
a little shrine, the red writing on the walls ("They spelled Marcus with a V. Nobody
tell Marcus."), the price list painted on the snack bar ("No pictures. How do you know
what a thing LOOKS like?") and its hanging sign ("Pictures! Finally."), the apartments,
the pointed jars and a cart wheel. **In the temple:** the statue ("Either he's dangerous or he sleepwalks"), the
offering bowl, the chests ("the best room I've ever been thrown out of"), the clerk's
table and his rack of rolls ("Cubbies!"), two braziers, the bronze tablets, the
standards, and the painter's cat, asleep on a chest ("SHE got in without a tunic.
Nobody scores cats."). Things worth looking at twice have a second line.

<!-- ROME-13W -->
**In the Forum** (round thirteen): Castor's temple ("A giant temple with a front porch like a
stage. Mom would have a play on up there by Friday."), Juturna's spring ("The fountain's
big quiet cousin."; splashed: "COLD. VERY cold. Two out of ten. I am now extremely awake."),<!-- PASS-17R: these two quoted as round seventeen has them -->
the garlands (Phyllis: "Hands off the merchandise, child. Smell with your nose. That part's
free."), the Tuscan street ("It smells like river. And a little bit like cows."), Caesar's
basilica in its scaffolding ("Like my science project."; "Mom has a rule about scaffolding.
It's the same as her rule about everything."), the Puteal ("like a well with no well in it.
Everybody walks AROUND it."), the moneychanger's table, set out with nobody minding it
("Somebody's coming RIGHT back."), the statues on their columns ("The pigeons are winning."),
the speakers' platform ("I'd talk about snacks. Nobody would leave. Nobody."), his own temple
at the far end ("My door guy is a dot." "The dot just folded its arms. I can tell from
HERE."), the gold roof, Moneta ("Rome puts temples on hills like candles on a cake."), the
record office ("a giant filing cabinet"), the basilica of Paullus ("A mall! Rome has a
MALL."), the hole where the senate house was ("Rome is getting a new tooth. A really big
one."), the crane ("Like a hamster. A STRONG hamster.") and the pigeons ("They commute.").
**On the Capitol**: the temple ("Rome is showing off."), the name on its front ("Q LVTATIVS
CATVLVS. Rome is STILL out of U's."), the roof ("It's GOLD."), the three doors ("something huge
and gold is sitting very still. I'll let it."), the altar ("A stone barbecue the size of a
minivan, and it's out. Just smoke. Dad would still poke it."), the dictator's chariot facing
the temple ("Valet parking for gods."), the man on the world ("Big Sis would have a
footnote."), the kings ("The sword guy looks busy.") and the dictator's new statue among them
("Hey, it's the guy from my coin! Same nose. He's EVERYWHERE today."), the bronze tablets ("More
terms and conditions."), the pen, the hut of Romulus ("Somebody's grandpa would NOT sell."), the
view, the theater ("Biggest bleachers EVER."), the Janiculum ("Trees that bring their own
shade."); a look at Moneta is written ("Like a camel that's really into temples.") and never
said, because Juno's temple on the hill's other summit is not in the picture (it would stand
behind the temple's right side, which runs out of it). **Across the Tiber**: the
river ("It's brown and it's in a hurry. Like a dog after a bath."), the barge ("a boat that's
mostly a table"), the bales of papyrus ("Big Sis would sniff it. She sniffs books."), the
landing ("Rome hides its stairs everywhere EXCEPT here."), the far bank, the road and the
gardens ("Somebody's got a REALLY big backyard."), the old man's house and its doorpost ("Like a
doorbell that doesn't ring."), his window, the house of prayer ("It looks like a place for
listening in."), the bench ("Sitting is the main part of waiting."), the well ("No more wishes
in water. I'm on a break."), the fig tree, the washing ("The laundry lady would have
OPINIONS.") and the hens (under "The chickens", below).

**The two new things, tried on the old people** (round thirteen). The Gaul's toga and
Phyllis's lamp have a line from each of the eight where one is worth it (the doorkeeper: "That
is not a toga. That is a large mistake. Take it off my steps."; the soothsayer: "A lamp for a
journey. A long one, over water. Not yours, I think."; the clerk: "An unlit lamp. In a
treasury, that is the only good kind. ...One."), and the Son's stock reply where not. In the
temple the lamp gets his own lines ("Post Felix's lamp through a time door? He'd end up
lighting it in the wrong century."). The Gaul's toga can never be carried into the temple:
the tunic needs the delivery, which needs the swap.

One thing is optional and has an ending of its own: the incense. Inside, he can set it
down at the god's feet ("Hi. This is from the chicken man outside. He says sorry about
the steps. And beware of today."), and the clerk, who took him for the incense boy all
along, loses count again.

Everyone is asked about Dad, and everyone answers in character. The doorkeeper: "Then
he is lost." "He's not lost. He's making good time. Somewhere." The keeper: "if he is in
Rome he will come here, so sit, wait, eat." The clerk: "Is he made of silver?" "No."
"Then I have not counted him." The soothsayer, asked whether he finds his father: "The
birds do not say. But boys who look, find. That is not prophecy. That is boys."

---

## The family's faith, and the Bible's history as history

Added on 7 October (`briefs/WEAVE.md`). The Son is ten and has been to Sunday school all
his life, and he has landed about forty years before the first Christmas. Nothing here gives,
takes or opens anything: it is what he knows, coming up where it would.

<!-- ROME-13W: five quotations since round thirteen -->
The rules it keeps. Scripture is quoted five times since round thirteen, word for word
from the King James Version, and the boy knows them all by heart (since round seventeen,
the author's rule of 16 October, nobody in Rome says chapter and verse aloud: the boy says
where he knows the words from, and the references are kept in this document and in
CHARACTERS.md; PASS-17R): by the date seller, the first clause of Micah 5:2 and Numbers 6:24; by his
father-in-law across the river, the first clause of Isaiah 40:31 and Numbers 6:25; and by
the boy himself, Numbers 6:26. Each ends on the King James mark where its verse runs on (a
comma, a colon, a semicolon, a colon), and the last on its full stop, where the blessing
ends. Everything else from the Bible is told in the speakers' own words. Nobody argues, nobody is
laughed at for what he believes, nobody is told what is coming. "Not yet." is said
three times in the act and no more (the check script counts). Nobody says "early":
that word is Little Sister's, in Act Four.

| Where | What happens | The lines |
| --- | --- | --- |
| The street, the first time (a cut-scene, above) | **B.C.** The keeper's cry gives him Caesar; Big Sister's timeline gives him B.C.; "before Christ" does the rest. Operation Don't Wreck Anything. | `rome.street.cry`, `rome.street.bc.1` to `.4` |
| The fountain, on taking the coin (#7) | **The coin.** The tribute money (Matthew 22:17-21), in his own words, with the point of it right. "This isn't that Caesar. Not yet." | `rome.fountain.caesar.1` to `.4` |
| The senator, asked "Does Caesar have a kid? A kid like that could get in ANYWHERE." (on offer once he has been to the street, until the senator leaves) | **Caesar's great-nephew.** "Caesar has no son. There is a great-nephew: Gaius Octavius, eighteen, off at his books in Apollonia." "Nobody gives the boy a thought. I mention him only because I am thorough." "I know another Caesar! Caesar AUGUSTUS. He counts everybody. It's how the Christmas story starts." <!-- PASS-17R: no "Luke 2:1." aloud since round seventeen --> "Augustus. There is no such name. I know every name in Rome that matters." "...Not yet." | `rome.senator.ask.caesar`, `rome.senator.ans.caesar.1` to `.5` |
| The clerk, asked "What's on all the wax pads?" | **Herod.** "Accounts. Judea's: Antipater's, and his son Herod's, from Galilee, where the young man governs." "Herod? KING Herod? The bad king in the Christmas story?" "Herod is no king. He is a procurator's son with expensive tastes. I have the figures." "...I'd count him twice. I'm just saying." (No tag here: three is the limit.) | `rome.clerk.ask.judea`, `rome.clerk.ans.judea.1` to `.4` |
| The stepping stones, looked at a second time | **The road.** "Paul walks into Rome on a road like this one day. It's on the map in the back of my Bible. Dotted line. Not yet." (Acts 28:15-16. Until round seventeen he also named the road, the Appian Way, from the map, and said the church came out to meet him: PASS-17R made it shorter, and his own.) | `rome.stones.look2` |
| The date seller | below | `rome.dateseller.*` (38 lines since round thirteen) |
| Across the river (round thirteen) | **Eleazar**, the date seller's father-in-law: below, "Eleazar, across the river" | `rome.eleazar.*` |

### The date seller

He stands at the kerb of the right-hand pavement, just up the street from the last
stepping stone, where people cross: at 492, 444, facing the fountain and past it. He is
in no painter's list; the place was chosen by eye and by measurement. Farther up the
pavement, where there is more room, the words of anyone speaking at the fountain, the
stepping stones or the boy's first stopping place were written across him (words go
over the speaker's head, and that is where his was). At the kerb the engine counts him
as standing beside the speaker and lifts the words over him. Words spoken at the
laundry and by the street boy still pass over him: there is no place up the street
where none do. His ground is blocked (the engine does it for anyone standing), his area
to click on touches no other, and he is 34 pixels clear of the fountain. The boy talks
to him from the roadway, at 446, 460, looking up.

Looked at: "A man with a beard and a basket of... giant raisins? He's the only one in
Rome who isn't in a hurry." And again: "He keeps looking the same way, past the fountain
and a long way off. Like he's waiting for somebody."

The first time: "Dates, young sir. From Jericho, in Judea. There are none better: I
have looked." "Jericho? The Jericho with the WALLS?" "You know of the walls. In those
shoes. ...The same Jericho. The palms have done better than the walls." That the boy
knows Jericho is why the man talks to him at all. <!-- PASS-17R: "In those shoes" (was "In that hat": he wears no cap) -->

| He asks | What is said | Notes |
| --- | --- | --- |
| "Can I try one? I'm between snacks." | "For a boy who knows of Jericho, the first is a gift. Here." He holds one out on his open hand; the boy takes it. "It's candy. It's candy that GROWS. Nine out of... OW. There's a rock in it!" "The stone. That part is a palm tree that has not begun. I ought to charge you for the tree." "Nine out of ten. One off for the surprise rock." | Once: one gift. It is eaten; nothing is carried away. |
| "Everybody here has a statue to pray to. Which one's yours?" | "None. We have one God: the God of Abraham, of Isaac and of Jacob. He made heaven and earth." "Abraham, Isaac and Jacob? I know those guys! He's our God too! We pray to Him at my house!" <!-- PASS-17R: they pray to Abraham's God, not to Abraham --> "At your house. ...Then the world is larger than Rome has told me." "Rome finds us Jews very funny: a great Temple in Jerusalem, and no statue in it." "Pompey himself went in, nineteen years ago. He found no image. Not one." "I ask them how they would carve the One who made the stone. They buy their dates and go." | The joke is his, told on himself. He says nothing about anybody else's gods. |
| "What do you pray for?" (on offer once the one above has been asked) | "For the one who is promised. Every day, facing Jerusalem. The prophet Micah has told us his town:" "'But thou, Bethlehem Ephratah, though thou be little among the thousands of Judah,'" The boy turns away, to us: "That was MY line! In the Christmas program! ...Bethlehem. I know SO much about Bethlehem." "I've never wanted to tell anybody anything so much. It's not mine to tell. That's the angels' job." <!-- PASS-17R: no "Micah 5:2!" aloud; a boy's words for the angels --> And back to the man: "Mister? It's going to be worth the wait. If I were you, I'd keep watching that town." A moment. "...That was not a guess. I will not ask you what it was. But I will watch." "And for you, young sir: 'The LORD bless thee, and keep thee:'" The boy's head goes down as it does every Sunday, hands folded, before he knows it has. "Whoa. That's how church ends! The very same words. ...Thanks, mister." <!-- PASS-17R: no "Numbers 6:24!" aloud --> | The heart of the act. Once: a blessing is not given twice for the asking. |
| "Bye, mister." | "Go well, young sir. Come any day but the seventh. That day I rest, and Rome always wants dates." | No weekday is named anywhere: the game does not say what day of the week the Ides fell on. |

<!-- ROME-13W -->
Since round thirteen he has one more line, said once, after his blessing or at his goodbye,
whichever comes first: "Across the river, by the stone bridge, my wife's father reads in the
house of prayer. Eleazar. Greet him for me." (`rome.dateseller.eleazar`). The Gaul's toga,
shown to him: "That is not the senator's, young sir. That toga could shelter a family. Mine,
for instance." The lamp: "A good little lamp. Whoever it is for, may it light a good house."

Things shown to him. The quarter: "A bird. An eagle? Whoever struck this was proud of
his bird. ...It is not silver, young sir." "A coin should go home. Every year we send
our offering to the Temple in Jerusalem: the half-shekel." The dead phone: "A black
stone, polished like a mirror. It shows me an old man selling dates. It is not wrong."
The senator's toga: "A senator's toga. I know the man. He buys the best dates in Rome
and remembers them as cheaper." The fountain coin: "Caesar. He has been a friend to us
Jews of Rome: we may meet, and keep our fathers' customs." "But that is fountain
silver, young sir. Somebody's wish. Not a price." The soothsayer's breakfast: "The
soothsayer's. Every day he offers to tell my fortune by his hens. Every day: not by
hens, thank you." (one line of the chickens' thread, below). The gum, the tunic and the
incense get the Son's stock replies.

Two things about how it is staged. The engine picks the gesture for each line from the
line's id, and the date seller has four: an open hand with a date on it, a finger
raised, a hand laid on his chest, a small shrug. The ids here were chosen with that in
mind (the blessing is said with the hand on the chest; "He found no image. Not one."
with the shrug), so renumbering them changes what his hands do. And the boy's hair,
which would not go down for the doorkeeper ("I've tried. Mom's tried. Gravity's tried."), stays up
for the blessing; his head is what goes down. That is the people artist's prayer pose,
and nobody mentions it.

### Eleazar, across the river (round thirteen)

<!-- ROME-13W -->
The author asked for a devout Jew of Rome who prays toward Jerusalem, knows the prophets and
waits for the Messiah. So the date seller's family has a home across the river, and the boy
meets its old man. The date seller's scene is about where the promised one will come from;
Eleazar's is about waiting for him. The boy is waiting too, for his father. Nothing in it
gives, takes or opens anything a puzzle needs, and the act does not wait for it (decision
5): the old man is simply there on his bench whenever the boy comes back. The music drops
for it, from his greeting to his "Go in peace", and the river is heard, very softly; nobody
shouts. It is staged slowly, with room round the words, as the date seller's blessing is.

Who he is (true to 44 B.C., or marked Probable in the history table below): a grown man in
Jerusalem when Pompey took the city, nineteen years ago; brought to Italy with many others,
bought, and in time freed by his master; he lives where his people live, across the river,
with his daughter, her husband Yose (the date seller) and their girl Mariam, and reads in
the house of prayer next door. He prays toward Jerusalem, where the Temple is, with his
window open that way, evening, morning and midday; tassels with a thread of blue hang at the
corners of his mantle; words of the Law are in a little case on his doorpost. His talk is
`eleazarTree` (`js/content/talk/rome.js`), and every hook in it is staging only.

| | What is said | Notes |
| --- | --- | --- |
| First sight | The arrival across the river (above): "He's praying. With his window open. Like Daniel." "I'll wait till he's done. ...I'm getting good at waiting." Mariam, if he asks her about the window first: "He's praying. He comes down when he has finished, and he does not hurry for anybody." | He is at his window until the boy has waited |
| The wait | The first click on him at his window, his house or door, his window, or the bench. The boy stands at the bench's near end facing the house (he cannot sit), and, a few seconds on, to us: "Waiting. I'm doing it. Look at me doing it." The old man steps back from the window, comes out of his door with his scroll (the boy steps aside), walks along the front of the bench and sits. | `rome.eleazarDown`. If the boy leaves by the bridge without waiting, the old man is on his bench when he comes back (since round fifteen, by the map as well) <!-- MAP-15D --> |
| Greeting | "Peace to you, child." Four ways in: "Peace to you too, mister."; "I waited the WHOLE time. I didn't fidget once. ...I fidgeted once." "Twice. But very politely."; "Is that your church? The one with the bench?" "A house of prayer." (and that is all); and, if he has met the date seller, "Do you know the date seller in the city? Beard, basket, VERY calm?" "Yose. My daughter's husband. Does he say the dates are selling?" "He says Rome always wants dates." "He always says so." Then: "I am Eleazar. And who are you, child, who waits so well?" "I'm lost. Well, my dad's lost. One of us is. I'm waiting for him to find me." "He always comes. He's late sometimes. He calls it making good time." "A father who always comes. That is a good thing to wait for." | `rome.metEleazar` |
| The window | "Praying, child. Toward Jerusalem, where the Temple is. In the evening, in the morning, and at midday." "Like Daniel! Window open, toward Jerusalem, three times a day. ...No lions, though. Right?" "No lions, child. Only Mariam. ...You have been well taught." <!-- PASS-17R: shorter, and he answers it --> | Daniel 6:10 and Psalm 55:17, told (and the lions' den, 6:16, asked about) |
| How he came to Rome | "I was a grown man in Jerusalem when Pompey took the city, nineteen years ago. Many of us were brought here." "I was bought, and I worked, and in time my master set me free." "...Now I live where my people live, across the river. And I pray toward home." "That's a long way from home. ...Me too. A REALLY long way." "Then we are neighbors in that, child." | Told without bitterness, and a pause |
| What he prays for | "For Jerusalem's peace. And for the one God has promised: a son of David, a king who will rule in righteousness." "His kingdom will have no end. And the prophet says the nations will come to his light." He looks over the river: "Greeks. Egyptians. Gauls. Romans. All of them, over there." "Even these. Even, perhaps, a boy in strange shoes." The boy turns to us: "There's an old man like him in my Bible. ...I'm not saying anything. I'm SO not saying anything." | Psalm 122:6; Isaiah 9:7 and 32:1; Isaiah 60:3, with 11:10 and 49:6: told. Simeon (Luke 2:25) is thought of, to us, and never named |
| The tassels | "Can I ask about your blanket? It's got strings on the corners. With blue in them." "Not a blanket, child, and not strings. The Law tells us to wear them, so that we remember." "Like a string on your finger! But holy." "...Yes. Very like that." | Numbers 15:38-39, told |
| The heart (on offer only after "What do you pray for?") | "What if he doesn't come in time? For you, I mean." "Then my grandchildren will see him, or theirs. The promise does not depend on an old man's eyes." "The prophet Isaiah says it: 'But they that wait upon the LORD shall renew their strength;'" "That's on our fridge! On a magnet, with an eagle. Mom reads it when Dad's late." <!-- PASS-17R: no "Isaiah 40:31!" aloud --> "Dad's late right now. REALLY late. I don't even know which year he's late in." "Then we are both waiting, child. Shall we wait together a little?" | QUOTED: Isaiah 40:31, to its semicolon |
| The prayer | "Okay. ...Yes. Together." (Or "I don't know the words you use." "Use your own, child. He knows them all."; or "Can we do it in a little bit? I should check on... everything." "Whenever you come back. I am not going anywhere, and neither is the promise.", and, when he comes back, "Mister Eleazar? Can we still wait together?" "Come. Stand here, beside me. We face the same way.") They stand side by side facing toward Jerusalem; the boy's head goes down and his hair stays up. "Dear God. Please help Dad find me. And please be with Mister Eleazar while he waits." "You know what he's waiting for. I know too. I didn't tell. Amen." "Amen." "You pray like one who knows him well." "We talk a lot. Mostly at bedtime." | `rome.prayed`. The boy prays in his own words. The old man gets up from his bench, slowly, and goes to stand by it facing the river, and Jerusalem beyond it; the boy stands beside him, a little nearer us, facing the same way; the old man's head goes down, and then the boy's |
| The blessing | "Come. Stand still a moment." His hand on the boy's head: "And for you, child: 'The LORD make his face shine upon thee, and be gracious unto thee:'" "That's the blessing! Pastor says it at the end of church! ...You only did the middle part. I know all THREE." <!-- PASS-17R: the design's own sample (office-hq-design.md, section 1) --> If the date seller has blessed him: "The date seller gave me the first part! You two are doing it in PIECES." "Yose blessed you too? Then the blessing has been walking all over Rome this morning." Then: "Mister Eleazar? Can I give you the last part?" "'The LORD lift up his countenance upon thee, and give thee peace.'" <!-- PASS-17R: "Numbers 6:26." no longer said after it --> "...From a child, at my own door. I will remember the day the blessing came back to me." "Go in peace, child. And find your father." | QUOTED: Numbers 6:25 (his), Numbers 6:26 (the boy's). The hand on the head as Jacob blessed Joseph's sons (Genesis 48:14), shown. `rome.blessed`. The old man steps to his left and turns to the boy; the boy stands before him on the same row, his head bowed; the hand is eased down onto his hair for the verse, and away after it |
| After | Walking away, to us: "I didn't tell him. It wasn't mine to tell. But I prayed it. That counts." A second talk, and every one after: "I am still waiting. It is easier this morning." | Nothing more on later visits. After "Go in peace" the old man goes back to his bench and sits, and the music comes back; the boy walks a few steps down the lane and turns to us for his last line |

The priestly blessing goes three ways (decision 4): verse 24 from the date seller in the
street, verse 25 from his father-in-law across the river, verse 26 from the boy, given back.

**Scripture quoted in the act**, King James Version, exact (until round seventeen each reference was said by the boy; since the author's rule of 16 October none is said aloud, and they are kept here: PASS-17R):

| Verse | The words quoted | Said by | Line | Status |
| --- | --- | --- | --- | --- |
| Micah 5:2, the first clause | "But thou, Bethlehem Ephratah, though thou be little among the thousands of Judah," | the date seller | `rome.dateseller.ans.pray.2` | **Checked** (facts-home, `kjv.mic5.2`) |
| Numbers 6:24 | "The LORD bless thee, and keep thee:" | the date seller | `rome.dateseller.bless.1` | **Checked** (facts-home, `kjv.num6.24-26`); read again 13 October, Bible Hub and Bibleserver |
| Isaiah 40:31, the first clause | "But they that wait upon the LORD shall renew their strength;" | Eleazar | `rome.eleazar.heart.2` | **Checked**: Bible Hub and Bibleserver, King James Version, read 13 October. The verse runs on, so the quotation ends on its semicolon |
| Numbers 6:25 | "The LORD make his face shine upon thee, and be gracious unto thee:" | Eleazar | `rome.eleazar.bless.1` | **Checked**: the same two, 13 October; facts-home |
| Numbers 6:26 | "The LORD lift up his countenance upon thee, and give thee peace." | the boy | `rome.eleazar.last.son` | **Checked**: the same two, 13 October; facts-home |

**The other touches of the faith thread in the new places:**

| Where | What | The lines |
| --- | --- | --- |
| The street, the date seller | His father-in-law reads in the house of prayer across the river: "Greet him for me." | `rome.dateseller.eleazar` |
| Across the Tiber, Felix and Corinth | The boy, to us: "Corinth! I KNOW Corinth! Paul lives in Corinth one day. He makes tents. There are TWO letters..." "...Operation Don't Wreck Anything." Felix: "...Are you all right? You went funny." "Fine! Corinth sounds GREAT. Ten out of ten. Would move to." (Acts 18:1-3 and 18:11, and the two letters to the Corinthians, in his own words.) | `rome.felix.paul.son.1`, `.2`, `rome.felix.paul`, `rome.felix.paul.son.3` |
| Across the Tiber, the house of prayer | "No statues, no pictures, nothing painted. A wide door and a bench. Like a library, but for praying." <!-- PASS-17R --> | `rome.tiber.prayerhouse.look` |
| Across the Tiber, the doorpost | Mariam: "Words of the Law. The Law says to write them on the doorposts. So we do." "Like a note on the fridge! But on the door. And forever." "What's a fridge?" "...A cold cupboard. With magnets." (Deuteronomy 6:9, told.) | `rome.tiber.doorpost.look`, `rome.mariam.doorpost.1` to `.3` |
| Across the Tiber, the window | "His window. Still open. He'll be back up there at midday, I bet. He's a three-times-a-day man." | `rome.tiber.window.look2` |
| Across the Tiber, the fig tree | Since round seventeen, no longer a touch of the thread: "A fig tree with tiny new leaves. A snack tree! Still loading. Come back in summer." (It was "Fig trees are all over my Bible.": a Bible fact tacked onto a look, which the author's rule of 16 October takes out. PASS-17R) | `rome.tiber.figtree.look` |

**What nobody says, across the river.** Eleazar never names Jesus; never speaks of a birth in
a stable, a virgin, a cross or a rising; never says the promised one is God; uses no
Christian word; names no year and no time when; says nothing against the Romans' gods; mocks
nobody; argues with nobody; is not converted, and nobody tries. The boy never tells him who
is coming, or when, or where (the date seller has had Bethlehem from Micah, and the boy kept
it to himself, and keeps it now), and never names Simeon. The one Christian word said to him
is the boy getting Rome wrong ("Is that your church?"), and the old man's whole answer is "A
house of prayer."

---

## The chickens, and the years

Added on the evening of 7 October, from the author's two rules (`briefs/DATING.md`) and
`briefs/WEAVE-2.md`. Four lines; nothing here gives, takes or opens anything.

**The chickens.** They are the thread through every era of the game: a chicken notices
a door in time before any person does, goes quiet, will not eat, and stands facing it.
Nobody explains it. Here they are the soothsayer's sacred chickens, which in Rome really
were kept for omens: if they would not eat, it was a bad sign.

| Where | What happens | The lines |
| --- | --- | --- |
| The soothsayer, asked "Why do you keep chickens in a cage?" before they have fed | This morning they will not touch their grain ("Today they will not touch a grain.", which was there), and he takes it for the worst of omens, as a man who sells omens would on the Ides of March: "The worst omen there is, and on the Ides. I sell omens, boy. This one I could not give away." | `rome.soothsayer.ans.birds.1`, `rome.soothsayer.ans.birds.omen` |
| The cage: the first time he calls them, or the second time he looks, fed or not. Once. | He notices it himself, and looks up the steps where they are looking: "...Huh. They're all facing up the steps. At the temple doors. Every single one. Chickens KNOW." Then he thinks of his little sister: "That's what my little sister says. She has a chicken called General Feathers. The General outranks me." He does not explain it. | `rome.birdcage.doors.1`, `.2` |
| The date seller, shown the soothsayer's breakfast | "The soothsayer's. Every day he offers to tell my fortune by his hens. Every day: not by hens, thank you." Courteous; nothing is said about anybody's gods. | `rome.dateseller.breakfast` |

Two things that were there already now belong to the thread. When it is calling them
that shows him, his old line at the cage ("They can tell I don't have snacks. Chickens
always know.") comes just before he sees what they do know. And when the breakfast comes
they eat the cookshop's bread,
which is not their grain ("They feed. Look at them feed."), and go on facing the doors:
whatever they know, they are still chickens. "Chickens KNOW." is Little Sister's. The Son
quotes her, once (the check script holds it), so in play order the player hears it first
from her brother, and from her own mouth in Act Three. General Feathers is in Dad's
suitcase in Act One: the Son does not know that, and the player does.

<!-- ROME-13W -->
**Mariam's hens** (round thirteen). Across the river the chickens have one more place:
Mariam's hens, which have stood in a row since first light, all facing the same way, over
the river, at the city, and will not eat and will not lay. Nobody in the game explains it.
(The door in time is over there, in the temple.) "Chickens KNOW." is not said again: the
hens get their own words. They face the way the old man prays.

| Where | What happens | The lines |
| --- | --- | --- |
| Across the Tiber, the hens: looked at, called, offered the breakfast | All in a row, facing the city; not one head turns ("Here, chick chick! ...Not one head turned. They've got somewhere to look."); they will not even turn round for the breakfast | `rome.hens.look`, `.look2`, `.use`, `.breakfast` |
| Mariam, asked about her hens | "They're in a ROW. They've stood like that since first light, all of them, looking over the river at the city." "They won't eat. They won't lay. Hens are sensible. Something over there is not." "Grandfather says hens don't pray. They only look." The boy, to us: "They're looking at my door. From the other side of a whole river." | `rome.mariam.hens.1` to `.3`, `rome.mariam.hens.son` (`rome.sawHens`) |
| Mariam, asked to ask one what's wrong | "You don't ASK a hen. You look her in the eye." "...She blinked. That means go away, I'm busy. She's not sick. She's busy." | `rome.mariam.crouch.1`, `.2` |
| The boy's little sister | "My little sister would LOVE you. You'd be bossy at each other." | `rome.mariam.boss.son` |

**The years.** Every year before Christ in the game is the Bible's own count, as
Archbishop Ussher counted it (`briefs/DATING.md`). Rome's own date, 44 B.C., is the same in
every count, and this act names no other year before Christ. The one thing about the act
that counted years from Egypt was the card before it, which reckoned from the old
textbook date of the pyramid; by the Bible's count Dad's Egypt is about 1920 B.C., and
the card is now to read "nearly nineteen hundred years later" (1921 to 44 B.C. is 1,877
years). The card that ends this act, "about two thousand years later", counts from Rome
to the present (44 B.C. to A.D. 2026 is 2,069 years) and stands. The boy's "Big Sis has
him on her timeline" agrees with her wall, which is made with Ussher's dates and names
44 B.C., the Ides of March (`home.timeline.6`). The check script now refuses a year B.C.
that is not in DATING.md's table, and anything in the act's files or this document that
leans on the old date.

---

## Ledger for this act

**People**

| Who | Where | Wants | Gives | Talks about |
| --- | --- | --- | --- | --- |
| Doorkeeper | steps, in the doors | a boy, a clean tunic, something for the god | the way in | the three things; what is inside; Dad |
| Soothsayer | steps, sitting | his breakfast, for him and for the birds | the incense box | the chickens; the temple; the boy's future |
| Senator | steps, until #2's delivery | his clean toga | his thanks, which the washerwoman honors; at the turn (round thirteen), the Gaul's toga | why he is late; the stain; Caesar's great-nephew; Dad; the Gaul |
| Snack-bar keeper | street, behind his counter | a boy with legs; since round thirteen, his boy home | a snack; since round thirteen, where his boy and the breakfast are (Titus hands it over) | the quarter; pizza; who owes him; Dad; his boy and the Ides ewe |
| Washerwoman | street, by her basket | the toga taken up the hill | the toga, then the tunic | how cloth is cleaned; the tunic; Dad; (round thirteen) her mix-up |
| Street boy | street, on the curb | to see the shoes light up again | hints, and a friend | the walnut game; the temple; what to do next; whose wish is in the fountain |
| Clerk | temple, at his table | to reach a number | nothing | what he counts; the statue's feet; the hum; the accounts from Judea; Dad |
| Date seller | street, at the kerb by the last stepping stone | nothing | one date, eaten on the spot; a blessing | the dates; his God; what he prays for; (shown the breakfast) the soothsayer's hens; his wife's father across the river |
| Gaulish senator (Gaius Iulius Litumarus) | the Forum, at the hoarding of the senate house's site; after #10, gone to the Senate | to know where the Senate meets today; his own toga | the senator's toga (#10) | the notice; the hole; the city's song; his mustache; why he will not go first |
| Garland seller (Phyllis) | the Forum, at the foot of Castor's temple | to give her son her lamp, and hear him say he will come | the lamp, then her leave (#12) | Anna Perenna's feast; her son and Corinth; the Twins' temple; her wish |
| Keeper's boy (Titus) | the Capitol, on a statue's base; after #11, gone home | to get down without saying he is stuck | the breakfast (#11) | the ewe; the geese and his feet; his father; who to ask |
| Goose-keeper (Anser) | the Capitol, behind his pen | nothing to happen to his geese; somebody to listen | the tale, which is the instructions (#11) | the night the geese saved the city; the dogs; his name; Moneta |
| Old man (Eleazar) | across the Tiber: at his window, then on his bench | nothing from the boy: he is waiting for the one God has promised | a prayer together; a blessing | the window; how he came to Rome; what he prays for; the tassels; waiting |
| Girl (Mariam) | across the Tiber, in the hen yard | her hens to finish looking | nothing | her hens; her grandfather; her father's dates; the doorpost |
| Boatman (Felix) | across the Tiber, between the landing and the barge | to sail for Corinth | his word (#12) | the barge and Ostia; Corinth; his mother; string |

**Things that are carried**

| Thing | Comes from | Used for | Leaves him |
| --- | --- | --- | --- |
| Senator's toga | the washerwoman (#1); since round thirteen, again from the Gaul (#10) | given to the senator (#2): the first time it is the Gaul's, and he gives it back | at #2 |
| Small tunic | the washerwoman (#3) | one of the doorkeeper's three (#6) | never: "Bring it back clean." |
| Soothsayer's breakfast | Titus, on the Capitol (#11; before round thirteen, the keeper, #4) | given to the soothsayer (#5) | at #5 |
| Incense box | the soothsayer (#5) | one of the doorkeeper's three (#6) | if he sets it down at the god's feet |
| Silver coin | the fountain (#7) | his mirror (#8); then, with Phyllis's leave (#12), tossed (#9) | at #9, to Nevada |
| Dead phone | his pocket | nothing. Tried on the hum, the sun, the door, and five people | never |
| Quarter | his pocket | nothing. The keeper cannot place the nose | never |
| Pack of gum | his pocket | nothing. The street boy likes it: "It's fighting back." | never |
| Gaul's toga | the senator, at the turn (#2) | given back to the Gaul (#10) | at #10 |
| Little clay lamp | Phyllis (#12) | carried across the Tiber to Felix (#12) | at #12, to Felix |

**Story facts the scripts keep**, besides the ten that are beats: `rome.knowsRule` (the
doorkeeper has said what he lets in), `rome.metSoothsayer`, `rome.metSenator`,
`rome.metUrchin`, `rome.metClerk` (first words said), `rome.sawStreet`, `rome.sawInside`
(arrival remarks made), `rome.knowsWash` (he has heard how cloth is cleaned),
`rome.offered` (the incense is at the god's feet), `rome.knowsBC` (he has heard the
keeper's cry and worked out when he is: it puts the question about Caesar on offer),
`rome.metDateSeller`. What the date seller has already given (the date, the blessing),
and what the boy has noticed at the cage, are kept by the lines themselves having been
said, as the engine counts them.

<!-- ROME-13W -->
Since round thirteen, besides the beats: `rome.wrongToga`, `rome.knowsSenate` (he has heard
where the Senate meets: from the senator or from Walnut), `rome.metGaul`, `rome.gaulAnswered`,
`rome.swapped`, `rome.knowsBoy`, `rome.metTitus`, `rome.metAnser`, `rome.knowsGeese`,
`rome.geeseGone`, `rome.knowsWish`, `rome.metPhyllis`, `rome.hasLamp`, `rome.metFelix`,
`rome.felixWord`, `rome.wishGranted`, `rome.eleazarDown`, `rome.metEleazar`, `rome.prayed`,
`rome.blessed`, `rome.metMariam`, `rome.sawHens`, and the arrivals `rome.sawForum`,
`rome.sawCapitol`, `rome.sawTiber`, with `rome.sawTheater` (he has looked at Pompey's theater
from the Capitol). Whether the date seller has blessed the boy is still kept by the line
having been said: the old man's "PIECES" reads it so.

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| "Step one: snacks." | The old arrival line | #4: "Step one: DONE." |
| "Step one is THAT way, past the bush." | The arrival: where the street is | The street: "Step one, I can SMELL you." |
| The door is inside, and shut | The arrival | #8 |
| Fourteen steps, counted upside down | Looking at the steps | #5: the soothsayer's knees |
| A score out of three | #6, asked early | #6, at the end: "Three out of three." |
| "I'll carry it by the corners." | #1 | The washerwoman's fact: "I'm going back to the corners." |
| The key-ring flashlight | Before the act (the pyramid) | #8: "I shined my flashlight at the hum, and POP: door." |
| Shiny | #7: the coin; the street boy's pot lid | #8 |
| Caesar's face on a new coin | The keeper's cry; the coin, read at the fountain; the keeper, shown it | Act Four, #6: Big Sister reads it |
| "The new has Caesar's nose on it" | The keeper's cry, the first time in the street | The street: "Caesar? JULIUS Caesar?"; #7: "So that's the nose the snack guy yells about." |
| The red mark on Big Sister's timeline | The street: "Before the red mark. That whole side is B.C." | Act Three: the timeline is on her wall, and she says what the mark is |
| B.C. is "before Christ" | The street | Act Four, in "Some when": what makes "Daddy's EARLY!" land |
| The Caesar coin, and whose picture is on it | #7, in the Son's words | Act Four: the same coin, and the verse, in Mom's |
| "Not yet." | #7 | The senator ("There is no such name."); the road |
| "It doesn't go down. ...Gravity's tried." | #6, to the doorkeeper | The date seller's blessing: his head goes down; the hair does not |
| A boy who knows the walls of Jericho | The date seller's first words | Why the man answers his questions; "...That was not a guess." |
| "Why is the sky DOWN?" | #8 | Act Four, #5: it fell out of the sky and hit his hat |
| "... It didn't come back down." | #9 (the old line) | Act Four, #5 |
| Dad's ketchup packets (his running gag) | CHARACTERS.md | #4: "He KNEW." |
| A dog, which he asks for every birthday | The dog asleep on the Forum: "Dad says we'll see. We never see." | #9 (the old line): "Edge, we get a dog." |
| "Dad says EVERYTHING is the wind." | The old line, at the hum | The clerk, about the noise by that wall at dawn: "That was... probably the wind." "That is what I decided." |
| The sacred birds will not touch their grain: "The worst omen there is" | The soothsayer, asked about the birds | #5: they feed on the cookshop's bread, and go on facing the doors |
| "Chickens always know." | The first call of the chickens | The same moment: they are all facing the temple doors. "Chickens KNOW." |
| "Chickens KNOW.", and General Feathers, who outranks him | The cage: his little sister's saying, and her chicken | Act Three: Little Sister says it herself, and the General's place on her pillow is kept. (Act One: the General is in Dad's suitcase. The Son does not know.) |
| "Bring it back clean." | #3 | Not yet. He still has the tunic. |
| A door the size of a coin, left open | #8 | Act Four: his family speaks into the Nevada end of it, and he answers (the letterbox), holding it open, he says, with Dad's keys in the sun; Little Sister posts a penny through it for him. Not yet: his end of it, which this act does not show. |
| A boy who would like to see the shoes light up again | The street | Not yet. Walnut is owed two nuts. |
| "He will be in the Forum, lost. They are always lost." | #2, the turn (round thirteen) | #10 |
| "The Senate meets today, in the hall beside Pompey's theater. I have a speech." | The senator (the old line) | #10: the answer to the Gaul ("He's giving a speech there. About drains.") |
| Pompey's theater, from the top of the hill | The Capitol's view ("Biggest bleachers EVER.") | #10: "Yes! I saw it from the top of the hill!" |
| The hole where the senate house was | The Forum ("Rome is getting a new tooth.") | #10: "There is the senate house. It is a hole with men in it." |
| "They light up when I stomp. Watch." and "Stomp when you go. So I can watch." | Walnut, in the street | #11: the stomp, on the Capitol (Walnut is not there to see it) |
| Every Ides the ewe | #4 (the keeper's errand, round thirteen) | #11: Titus, "She had ribbons. She went up the hill like a senator." |
| The goose-keeper's one story: "They cannot abide anything strange." | #11 | #11: "I'm the strangest thing in Rome. Watch my feet." |
| "I'll pay it back with interest. Interest is extra wishes." | #7 (the kept line) | #12: "Borrowed. Paid back. With interest. I TOLD Walnut interest is extra wishes." |
| "That's somebody's wish, you know." | #7 (the kept line) | #7, since round thirteen: whose (Phyllis's); #12 |
| "Corinth. That rings a bell. A big one. ...It'll come to me." | Phyllis (#12) | Felix: "Corinth! I KNOW Corinth! Paul lives in Corinth one day." |
| Carried like an egg | Phyllis's bundle ("wrapped up like an egg") | "I'll carry it like an egg."; the Gaul: "Carried like an egg. Somebody loves whoever that is for." |
| "Whoa. That's how church ends!" <!-- PASS-17R: was "Numbers 6:24! Pastor says that at the end of church." --> | The date seller's blessing | The old man's: Numbers 6:25, and the boy gives back 6:26: "You two are doing it in PIECES." |
| "Mister? It's going to be worth the wait." | The date seller | The old man, who is waiting: "You know what he's waiting for. I know too. I didn't tell." |
| "I'll wait till he's done. ...I'm getting good at waiting." | The arrival across the river | "Waiting. I'm doing it."; "Then we are both waiting, child." |
| Dad's ketchup | #4 ("He KNEW.") | The keeper, once Titus is home: "I won't even ask about the ketchup. I've grown as a person." |
| Mariam's hens face the city | Across the Tiber | Nothing: nobody explains the chickens |

---

## History: every statement made in the act

The rule is the one in [CHARACTERS.md](CHARACTERS.md): people of the time are never
wrong about their own time, and nothing goes down as **Checked** from memory. Each row
of the first table was read in the source named, on 2026-10-06. **To check** means
believed right and not confirmed. `briefs/LEVEL-rome.md` lists most of these as true;
the last column says whether this draft found them in a source.

The second table, further down, holds the statements added on 7 October with the
family's faith: the Bible's history, and Rome's where it touches it. A third, after it,
holds those of the four lines of the chickens, added that evening.

| The statement | Who says it, and where | Status |
| --- | --- | --- |
| It is the Ides of March, 44 B.C. | The era card; the soothsayer, `rome.soothsayer.hi.1` to `.3` | **Checked.** Wikipedia, Assassination of Julius Caesar: "assassinated on the Ides of March (15 March), 44 BC". |
| A soothsayer warned against the Ides of March | The soothsayer, `rome.soothsayer.hi.1` | **Checked.** Same page: "a seer had warned Caesar that his life would be in danger no later than the Ides of March". In the game he warns everybody, names nobody, and does not know why. |
| The Senate meets today in the hall beside Pompey's theater | The senator, `rome.senator.ans.late.1` | **Checked.** Same page: "during a Senate session at the Curia of Pompey, located within the Theatre of Pompey". ("Beside" is the design's word; the hall was part of the theater's buildings.) |
| The temple is Saturn's, and holds the treasury of the Roman People | The doorkeeper, `rome.arrive.out`, `rome.doorkeeper.ans.what.1`; the clerk, `rome.clerk.ans.count.1` | **Checked.** Wikipedia, Temple of Saturn: "His temple housed the treasury, the aerarium, where the Roman Republic's reserves of gold and silver were stored." |
| The statue's feet are tied with bands of wool, untied once a year at his festival in December | The clerk, `rome.clerk.ans.feet.1` | **Checked.** Same page: "The legs were covered with bands of wool which were removed only on December 17, the day of the Saturnalia." The same page says the statue "was veiled and equipped with a scythe" and "made of wood and filled with oil": the Son's "blanket on his head and a hook knife" fits, and nobody in the game says what it is made of. |
| Boys serve at the rites, and they come from good families | The doorkeeper, `rome.doorkeeper.rule.1`; the street boy, `rome.urchin.ans.temple.1` | **Checked.** Metropolitan Museum of Art, "Bronze statue of a camillus (acolyte)": "an attendant at sacrifices who was chosen from the noblest families". |
| A citizen on public business wears a toga; ordinary dress is a tunic | The senator, `rome.senator.toga.2`; the doorkeeper's "clean tunic" | **Checked.** Wikipedia, Toga: "formal wear for male Roman citizens"; "worn over a tunic". |
| Cloth is cleaned by treading it in tubs with stale urine | The washerwoman, `rome.washer.ans.white.1` | **Checked.** Wikipedia, Fulling: "In Roman times, fulling was conducted by slaves working the cloth while ankle deep in tubs of human urine." "Stale urine, known as wash or lant, was a source of ammonium salts and assisted in cleansing and whitening the cloth." (Wikipedia's page Fullo is more careful: "sometimes including ammonia derived from urine".) |
| A street snack bar has a masonry counter with big jars sunk in it | Seen; the Son, `rome.snackbar.look` | **Checked.** Wikipedia, Thermopolium: "a counter with holes where four jars were set into it (dolia) for food or wine". The Son calls them soup jars; the page says dried food or wine. He may be wrong. |
| It sells bread, sausage, cheese and hot food | The keeper, `rome.keeper.errand.2`, `rome.keeper.ans.pizza.3`; the soothsayer | Bread and hot food: **Checked.** Wikipedia, Popina: "a limited menu of simple foods (olives, bread, stews)". Sausage in Rome by this date: **Checked.** Wikipedia, Lucanica (Cicero mentions it). Cheese at such a bar: **To check.** |
| There are no tomatoes | The keeper, `rome.keeper.hi.5`, `rome.keeper.ans.pizza.5` | **Checked.** Wikipedia, Tomato: "The Spanish introduced tomatoes to Eurasia in the Columbian exchange in the 16th century." |
| Sacred chickens tell omens by how they feed; they are kept in a cage and offered bread | The soothsayer, `rome.soothsayer.ans.birds.1`, `rome.soothsayer.fed.3` | **Checked.** Wikipedia, Augury: "The chickens were kept in a cage under the care of the pullarius ... threw at them some form of bread or cake." "If the chickens refused to come out or eat ... the signs were considered unfavourable." In history a keeper consulted them for magistrates and generals; a soothsayer on the steps owning a cage of them is the design's liberty. |
| The silver coin is the denarius | The clerk, `rome.clerk.ans.count.1` | **Checked.** Wikipedia, Roman currency: "the denarius remained the backbone of the Roman economy". |
| New coins this year carry Caesar's own face | The keeper, `rome.keeper.coin.1` | **Checked.** Same page: "Julius Caesar issued coins bearing his own portrait"; "The appearance of Caesar's portrait on Roman denarii in 44 BC". |
| Streets have raised sidewalks and stepping stones | Seen; the Son, `rome.stones.look` | **Checked**, in a popular source. My Modern Met, on Pompeii: "These prominent stepping stones acted as ancient crosswalks"; "Raised sidewalks with drainage". |
| Children play a game with walnuts: a little pile, knocked down with a thrown nut | The street boy, `rome.urchin.ans.game.1` | **Checked**, in a secondary source. Brewminate, "Nuts and Knucklebones: Toys and Games in Ancient Rome": "building a pyramidal structure with a base of three nuts and a fourth nut placed on top. The players would then attempt to knock down the structure with another nut." That the winner keeps the nuts: **To check.** |
| Accounts are written on wax tablets | Seen; the clerk, `rome.clerk.phone.1` | **Checked.** Wikipedia, Wax tablet: "from taking down students' or secretaries' notes to recording business accounts". Not on the level's list: it comes from the scene brief. |
| Notices are posted on the base of the temple | Seen; the Son, `rome.board.look` | **Checked.** Wikipedia, Temple of Saturn: "The temple's podium, constructed out of concrete covered with travertine, was used for posting bills." Not on the level's list: the painter's. |
| The treasury also keeps the laws, the legions' standards and the official scale | Seen: tablets on the walls, standards in the corner, the clerk's balance; the Son, `rome.tablets.look`, `rome.standards.look`, `rome.table.look` | **Checked.** Same page: "The state archives and the insignia and official scale for the weighing of metals were also housed there." Wikipedia, Aerarium: "including Roman laws and senatus consulta"; "It also held the standards of the Roman legions". That the laws hung on its walls as bronze tablets: **To check.** Not on the level's list: from the scene brief. |
| Money comes to the treasury in sealed sacks, by a low door in the temple's base | Seen; the Son, `rome.cart.look` | **To check.** Wikipedia, Aerarium, puts the treasury "below the Temple of Saturn"; the door, the cart and the sacks are the painter's. Not on the level's list. |
| There is a February before March | The soothsayer, `rome.soothsayer.hi.5` | **To check.** Not on the level's list. |
| Rome has consuls, and people know their faces | The keeper, `rome.keeper.ans.pay.1` (the design's own line) | **To check.** |

### Added on 7 October: the Bible's history, and Rome's where it touches it

Every statement the fifty-five new lines make. "facts-home" is `briefs/out/facts-home.md`,
the checker's report of 7 October, where each item was read in the sources it names and
each verse in two King James copies; the id in brackets is its heading there. "Read
2026-10-07" is this writer's own reading, for the few things that are not on the
checker's list. Scripture the game QUOTES is marked so; everything else from the Bible
is in the Son's own words, or the date seller's.

| The statement | Who says it, and where | Source, and status |
| --- | --- | --- |
| The new silver has Caesar's portrait on it, and the old has not | The keeper, `rome.street.cry` | **Checked.** The row above ("New coins this year carry Caesar's own face"). |
| The Caesar on the money is Julius Caesar, and his time is B.C. | The Son, `rome.street.bc.1` | **Checked**: it is 44 B.C. (the first row above). That he is on Big Sister's timeline "before the red mark" is the home act's to keep true (`home.timeline.bigsis`: "At the red mark the years turn round. Before it they count down: B.C."). **Confirmed with the home act** as it stood on the evening of 7 October: her wall is made with Ussher's dates and names "44 B.C.: the Ides of March. That one is Rome's." (`home.timeline.6`). |
| B.C. means "before Christ", and it is counted back from the birth of Jesus | The Son, `rome.street.bc.2` | **Checked.** facts-home (`time.bc.ad`): Britannica, Christian Era. |
| So Jesus has not been born, and there has been no Christmas | The Son, `rome.street.bc.2`, `.3` | **Checked.** facts-home (`time.bc.ad`, `time.jesus.birth`: probably about 6 to 4 B.C.). The Son gives no number of years. |
| The coin has the name CAESAR on it | The Son, `rome.fountain.caesar.1` | **Checked**, read 2026-10-07. WildWinds, Julius Caesar: the portrait denarii of 44 B.C. read CAESAR IMP, CAESAR DICT QVART, CAESAR DICT PERPETVO: every one bears the name. Wikipedia, Julius Caesar: "shows Caesar's laurelled head surrounded by the CAESAR DICT PERPETVO". Not on the checker's list. |
| The tribute money: they ask Jesus about paying taxes to Caesar; He has a coin shown Him and asks whose image is on it; "Caesar's"; give Caesar what is Caesar's and God what is God's | The Son, `rome.fountain.caesar.2`, `.3`, in his own words | **Checked.** Matthew 22:19-21, facts-home (`kjv.matt22.19-21`). The question itself is verse 17 ("Is it lawful to give tribute unto Caesar, or not?"): read 2026-10-07, Bible Hub, King James Version. "Which is everything. Me included." is the boy's own. |
| The Caesar of that story is a later Caesar than this one | The Son, `rome.fountain.caesar.4` | **Checked.** facts-home (`rome.denarius.penny`): the emperor then was Tiberius (born 42 B.C., emperor A.D. 14 to 37). The Son names nobody. |
| Caesar has no son | The senator, `rome.senator.ans.caesar.1` | **Checked** for a son in law, read 2026-10-07: Wikipedia, Julius Caesar: "his only legitimate child, Julia" (she died in 54 B.C.). The same page lists Caesarion, Cleopatra's son, born in 47 B.C., as "unacknowledged". A Roman senator would say it as he does; the wording is the brief's. |
| His great-nephew Gaius Octavius is eighteen, and away at his studies at Apollonia | The senator, `rome.senator.ans.caesar.1` | **Checked.** facts-home (`rome.octavius`): Suetonius, Augustus 4, 5 and 8. |
| Nobody in Rome thinks of him as Caesar's heir | The senator, `rome.senator.ans.caesar.2` | **Checked.** facts-home (`rome.octavius`): the will that adopted him was read after Caesar's death (Suetonius, Julius 83). The senator does not call him an heir; nobody does. |
| The Bible has a Caesar Augustus, who has everybody counted, and the Christmas story begins with him | The Son, `rome.senator.ans.caesar.3`, in his own words (with the reference until round seventeen: PASS-17R) | **Checked.** Luke 2:1, facts-home (`kjv.luke2.1`): "a decree from Caesar Augustus, that all the world should be taxed" ("taxed" is the King James word for enrolled). |
| There is no such name as Augustus, this morning | The senator, `rome.senator.ans.caesar.4` | **Checked.** facts-home (`rome.octavius`): the Senate gave him the name in 27 B.C. (Suetonius, Augustus 7.2). |
| Antipater has charge of Judea, and his son Herod, a young man, governs Galilee | The clerk, `rome.clerk.ans.judea.1` | **Checked.** facts-home (`rome.herod.galilee`): Josephus, Antiquities 14.143 and 14.158. No age is given for Herod, as the checker asks. |
| Antipater is a procurator | The clerk, `rome.clerk.ans.judea.3` | **Checked.** The same: "so he made him procurator of Judea" (Whiston's Josephus). |
| Their accounts are on a clerk's table in the treasury at Rome | The clerk, `rome.clerk.ans.judea.1` | **To check.** The brief's invention. (Pompey made Judea pay tribute to Rome, as this writer remembers Josephus; that was not read today, and where such accounts were kept is not known to him.) |
| Herod has expensive tastes | The clerk, `rome.clerk.ans.judea.3` | The clerk's opinion, and the brief's line. Not sourced for 44 B.C. |
| Herod is not a king | The clerk, `rome.clerk.ans.judea.3` | **Checked.** facts-home (`rome.herod.galilee`): named king by the Senate in 40 B.C. |
| A King Herod is the bad king of the Christmas story | The Son, `rome.clerk.ans.judea.2` | **Checked.** Matthew 2:1, facts-home (`kjv.matt2.1`): "in the days of Herod the king"; that it is the same Herod, facts-home (`rome.herod.galilee`). |
| Paul came into Rome by road (and, until round seventeen, the brethren came out along it to meet him) | The Son, `rome.stones.look2`, in his own words | **Checked.** Acts 28:15-16, facts-home (`kjv.acts28.15-16`). That his journey is on the map in the back of the boy's Bible is the family's own. <!-- PASS-17R --> |
| The road was the Appian Way | The Son, `rome.stones.look2`, until round seventeen (PASS-17R: the line no longer names the road) | **Checked.** facts-home (`rome.appian`): Acts names two stations on it (Appii forum, The three taverns) and not the road. So the boy had the name from the map in his Bible, and said so. |
| Jericho is famous for its dates | The date seller, `rome.dateseller.hi.1` | **Checked.** facts-home (`rome.jericho.dates`): Strabo 16.2.41; Josephus, Wars 4.468. "None better" is a seller's opinion. |
| The walls of Jericho fell | The Son, `rome.dateseller.hi.2`; the date seller, `.hi.3` | **Checked**, read 2026-10-07: Joshua 6:20, Bible Hub, King James Version ("the wall fell down flat"). An allusion, in their own words; not on the checker's list of verses, and nothing is quoted. |
| A date has a stone in it, from which a palm grows | The date seller, `rome.dateseller.ans.try.3` | Common knowledge. |
| The Jews have one God, the God of Abraham, Isaac and Jacob, who made heaven and earth | The date seller, `rome.dateseller.ans.god.1`, in his own words | **Checked**, read 2026-10-07: Exodus 3:6 and 3:15, Bible Hub, King James Version ("the God of Abraham, the God of Isaac, and the God of Jacob"); "which made heaven and earth", Psalm 121:2, facts-home (`kjv.ps121.1-2`). |
| The family prays to the same God | The Son, `rome.dateseller.ans.god.2` | The family's own faith (`briefs/WEAVE.md`). |
| The Temple in Jerusalem has no statue in it | The date seller, `rome.dateseller.ans.god.4` | **Checked.** facts-home (`rome.pompey.no.image`): Tacitus, Histories 5.9, and 5.5 ("they do not allow any images to stand in their cities, much less in their temples"). |
| Rome finds that funny | The date seller, `rome.dateseller.ans.god.4` | **To check** for 44 B.C. itself. Cicero is contemptuous in 59 B.C. (facts-home, `rome.jews.in.rome`); Tacitus's "the shrine had nothing to reveal" is 150 years later. It is the brief's ("a Roman joke about a people who have a temple with no statue in it"). |
| Pompey went into the Temple nineteen years ago and found no image | The date seller, `rome.dateseller.ans.god.5` | **Checked.** facts-home (`rome.pompey.temple`: Josephus, Antiquities 14.71-73, 63 B.C.; `rome.pompey.no.image`: Tacitus). 63 less 44 is 19. |
| He prays every day, facing Jerusalem | The date seller, `rome.dateseller.ans.pray.1` | The custom is Scripture's: Daniel 6:10, facts-home (`kjv.dan6.10`): "his windows being open in his chamber toward Jerusalem". That a Jew in Rome in 44 B.C. did so: **to check** (the brief's). |
| His people wait for one who is promised, and the prophet Micah names his town | The date seller, `rome.dateseller.ans.pray.1` | **Checked.** Micah 5:2, facts-home (`kjv.mic5.2`). |
| **QUOTED:** "But thou, Bethlehem Ephratah, though thou be little among the thousands of Judah," | The date seller, `rome.dateseller.ans.pray.2`; the Son's answer, `.ans.pray.3` (with the reference until round seventeen: PASS-17R) | **Checked**, exact: Micah 5:2, the first clause, facts-home (`kjv.mic5.2`). The verse runs on, so the quotation ends on its comma. |
| Angels bring the news of that birth | The Son, `rome.dateseller.ans.pray.4` | **Checked**, read 2026-10-07: Luke 2:9-13, Bible Hub, King James Version. An allusion, in his own words; not on the checker's list of verses. |
| **QUOTED:** "The LORD bless thee, and keep thee:" | The date seller, `rome.dateseller.bless.1`; the Son's answer, `.bless.2` (with the reference until round seventeen: PASS-17R) | **Checked**, exact: Numbers 6:24, facts-home (`kjv.num6.24-26`). The verse ends with a colon, and so does the quotation. |
| That blessing is said at the end of church | The Son, `rome.dateseller.bless.2` | The family's own church. |
| He keeps the seventh day, and does not sell on it | The date seller, `rome.dateseller.ans.bye` | **Checked.** facts-home (`rome.sabbath`): Horace, Satires 1.9; Dolabella's letter of 43 B.C., in Josephus, Antiquities 14.225-227. No day of the week is named in the game. |
| Every year the Jews of Rome send an offering to the Temple in Jerusalem: the half-shekel | The date seller, `rome.dateseller.quarter.2` | **Checked, with the checker's wording.** facts-home (`rome.temple.tax`, "true with a change"): the sentence is its safe line for a Jewish character, word for word. No Roman in the game uses the word. |
| There are Jews living in Rome | The date seller, `rome.dateseller.coin.1`; he is one | **Checked.** facts-home (`rome.jews.in.rome`): Cicero, Pro Flacco 66-67 (59 B.C.). |
| Caesar has let them meet, and keep the customs of their fathers | The date seller, `rome.dateseller.coin.1` | **Checked.** facts-home (`rome.jews.in.rome`): Josephus, Antiquities 14.213-216 ("I permit these Jews to gather themselves together, according to the customs and laws of their forefathers"). "A friend to us" is his own judgment; Suetonius (Julius 84) has the Jews of Rome mourning Caesar for nights together. |

The statements the four lines of the chickens add (the evening of 7 October, `briefs/DATING.md`):

| The statement | Who says it, and where | Source, and status |
| --- | --- | --- |
| Sacred chickens that will not eat are the worst of omens | The soothsayer, `rome.soothsayer.ans.birds.omen` | **Checked** that it is a bad omen: the row in the first table ("Sacred chickens tell omens by how they feed"), Wikipedia, Augury: "If the chickens refused to come out or eat ... the signs were considered unfavourable." "The worst there is" is his own judgment, and so is "I sell omens" (a soothsayer on the steps owning the cage is the design's liberty, as that row says). |
| It is the Ides | The soothsayer, `rome.soothsayer.ans.birds.omen` | **Checked**: the first row of the first table. |
| A chicken notices a door in time before any person does, and stands facing it | The Son, `rome.birdcage.doors.1` (seen, and not explained) | The author's rule for this game (`briefs/DATING.md`, "Chickens know"). Not history, and nobody in the game says it is. |
| His little sister has a chicken called General Feathers, who outranks him, and she says "Chickens KNOW." | The Son, `rome.birdcage.doors.2`, `.doors.1` | The family's own (`briefs/DATING.md`; `docs/CHARACTERS.md`, Little Sister). |
| The soothsayer offers to tell the date seller's fortune by his hens, and he declines | The date seller, `rome.dateseller.breakfast` | His own choice, lightly put. Behind it, as this writer remembers it: the Law forbids divination (Deuteronomy 18:10-11; Leviticus 19:26). Nothing is quoted and no verse is named on screen. **To check** (not read today, and not on the checker's list). |

Sources for this table, beyond `briefs/out/facts-home.md` and the sources it names:
WildWinds, [Julius Caesar](https://www.wildwinds.com/coins/imp/julius_caesar/i.html);
Wikipedia, [Julius Caesar](https://en.wikipedia.org/wiki/Julius_Caesar),
[Roman Republican currency](https://en.wikipedia.org/wiki/Roman_Republican_currency);
Bible Hub, King James Version: [Joshua 6:20](https://biblehub.com/kjv/joshua/6-20.htm),
[Exodus 3](https://biblehub.com/kjv/exodus/3.htm), [Matthew 22](https://biblehub.com/kjv/matthew/22.htm),
[Luke 2](https://biblehub.com/kjv/luke/2.htm).

Sources for the first table: Wikipedia, [Assassination of Julius Caesar](https://en.wikipedia.org/wiki/Assassination_of_Julius_Caesar),
[Temple of Saturn](https://en.wikipedia.org/wiki/Temple_of_Saturn), [Toga](https://en.wikipedia.org/wiki/Toga),
[Fulling](https://en.wikipedia.org/wiki/Fulling), [Fullo](https://en.wikipedia.org/wiki/Fullo),
[Thermopolium](https://en.wikipedia.org/wiki/Thermopolium), [Popina](https://en.wikipedia.org/wiki/Popina),
[Lucanica](https://en.wikipedia.org/wiki/Lucanica), [Tomato](https://en.wikipedia.org/wiki/Tomato),
[Augury](https://en.wikipedia.org/wiki/Augury), [Roman currency](https://en.wikipedia.org/wiki/Roman_currency),
[Wax tablet](https://en.wikipedia.org/wiki/Wax_tablet), [Aerarium](https://en.wikipedia.org/wiki/Aerarium);
the Metropolitan Museum of Art,
[Bronze statue of a camillus (acolyte)](https://www.metmuseum.org/art/collection/search/246701);
My Modern Met, [Pompeii's ancient roads had raised crosswalks](https://mymodernmet.com/pompeii-roads);
Brewminate, [Nuts and Knucklebones: Toys and Games in Ancient Rome](https://brewminate.com/nuts-and-knucklebones-toys-and-games-in-ancient-rome/).

### Added in round thirteen: the bigger Rome

<!-- ROME-13W -->
Every statement the new lines make. The design's own table (`briefs/out/rome2-design.md`,
section 7) and its notes (`briefs/out/rome2-facts.md`) were read on 8 October; "read 13
October" is this writer's own reading, through a tool that fetches a page and reports on it
with quotations. "P&A" is Platner and Ashby's *Topographical Dictionary of Ancient Rome*
(1929), on LacusCurtius. Each fact, with every line that leans on it, is also in the writer's
facts note for the round (`facts.md`, kept with the round's working papers).

| The statement | Who says it, and where | Source, and status |
| --- | --- | --- |
| Saturn's temple stands at the far end of the Forum, at the foot of the hill; the road up the hill goes round behind it | The Son, `rome.forum.arrive.2`, `rome.forum.saturn.look`, `rome.hill.look` | **Checked.** P&A, "Aedes Saturni"; "Clivus Capitolinus" (the road "skirts the north front and the west side of the temple of Saturn") |
| Jupiter's temple on the Capitol has a roof of gilt bronze, three rooms with the god's in the middle, a statue of gold and ivory, and the great altar before its steps | The Son, `rome.forum.arrive.3`, `rome.forum.jupiter.look`, `rome.capitol.roof.look`, `.doors.look`, `.altar.look` | **Checked.** P&A, "Aedes Jovis Capitolini". Six columns across its front and three doors are the picture's: Probable |
| Catulus's name is over the entrance | The Son, `rome.capitol.name.look` | **Checked.** P&A. The exact words are unknown: the line reads only the name |
| The new senate house is going up where the old one was pulled down | The Son, `rome.forum.site.look`; the Gaul, `rome.gaul.who.5`, `.house.1`; Walnut, `rome.urchin.tip.gaul` | **Checked.** Dio 44.5 (Cary); P&A, "Curia Julia" (begun in 44 B.C.) |
| Caesar's basilica is unfinished, in scaffolding | The Son, `rome.forum.julia.look`, `rome.forum.scaffold.look` | **Checked.** P&A, "Basilica Julia" (dedicated unfinished in 46 B.C.) |
| The speakers' platform, with bronze beaks along its front and statues on it | The Son, `rome.forum.rostra.look` | **Checked** (Dio 43.49; P&A, "Rostra"). The rams on the new platform: Probable |
| Castor's temple has a front like a platform; it is the Twins'; the city's weights and measures are kept in it | The Son, `rome.forum.castor.look`; Phyllis, `rome.phyllis.twins.1`, `.2` | **Checked.** P&A, "Aedes Castoris" |
| Juturna's spring, a pool by Castor's temple | The Son, `rome.forum.spring.look` | **Checked** that it is there (P&A); its basin's look: Probable |
| The Puteal, a stone ring like a well's kerb; moneylenders' tables by it | The Son, `rome.forum.puteal.look`, `rome.forum.table.look` | **Checked.** P&A, "Puteal Libonis" (nobody says the lightning) |
| The basilica of Paullus, with shops, still being built | The Son, `rome.forum.paullus.look`, `.look2` | **Checked (secondary).** Plutarch, *Caesar* 29; Wikipedia, "Basilica Aemilia", read 13 October: begun about 55 B.C., "completed by 34 BCE by Paullus's son"; "the shops lining the southern end of the basilica" |
| A crane with a wheel a man walks in | The Son, `rome.forum.crane.look` | **Probable.** Wikipedia, "Treadwheel crane", read 13 October: "primarily used during the Roman period"; the reliefs that show one are later |
| The record office, a row of arches built into the hill | The Son, `rome.forum.records.look` | **Checked.** P&A, "Tabularium" |
| Juno's other temple, Moneta, on the hill's other summit, where the money is made; people call her the Warner; "money" comes from Moneta | The goose-keeper, `rome.anser.moneta.1`, `.3`, `rome.anser.coin`; the Son, `rome.anser.moneta.son`, `rome.forum.moneta.look` (and `rome.capitol.moneta.look`, written and never said: Moneta is not in the Capitol's picture) | **Checked.** P&A, "Aedes Junonis Monetae"; Etymonline, "money". Moneta from "warning" is doubted today: he says only that people call her so |
| It is Anna Perenna's feast: the city goes out to picnic on the grass by the river | Phyllis, `rome.phyllis.cry`, `.anna.1`, `.2`; Felix, `rome.felix.mother.1` | **Checked.** The calendar of Antium ("Ides. To Anna Perenna."); Ovid, *Fasti* 3 (Kline) |
| Violets, laurel and myrtle for sale in March | Phyllis, `rome.phyllis.cry` | **Probable** (the design's season) |
| The new silver carries the dictator's own head | Phyllis, `rome.phyllis.wish.2`; the Gaul, `rome.gaul.coin`; Eleazar, `rome.eleazar.coin` | **Checked.** The row above ("New coins this year carry Caesar's own face") |
| Romans threw coins into water with a wish | Walnut, `rome.fountain.wish.3`; Phyllis, `rome.phyllis.wish.1` | **Checked** for the custom (Suetonius, *Augustus* 57.1); the fountain's coins are the act's own |
| The dictator is building Corinth again, mostly for freedmen; it has lain empty a hundred years | Phyllis, `rome.phyllis.son.2`, `.3`; Felix, `rome.felix.corinth.1`, `.2` | **Checked.** Strabo 8.6.23 (Jones); Wikipedia, "Battle of Corinth (146 BC)"; *Electrum*, "Corinth after 44 BC". When the colonists sailed is not known, and no day is named |
| Corinth has a sea on each side | Felix, `rome.felix.corinth.2`, `.3` | **Checked (secondary).** Wikipedia, "Ancient Corinth", read 13 October: the Corinthian Gulf to its west, the Saronic Gulf to its east, a harbour on each |
| Barges take cargo between Rome and Ostia, where the big ships wait off the shore | Felix, `rome.felix.where`, `.table`, `.ostia.1` to `.3` | **Checked.** Strabo 5.3.5 (Jones) |
| Papyrus and linen from Egypt | Felix, `rome.felix.carry`, `.ostia.2`; the Son, `rome.tiber.bales.look` | **Probable** (Pliny, *Natural History* 13: not read) |
| The ninth hour | Felix, `rome.felix.word.1`; Phyllis | **Checked (secondary).** Wikipedia, "Roman timekeeping", read 13 October: twelve hours from sunrise to sunset; the ninth about 3 p.m. |
| The sacred geese of Juno are kept on the Capitol and fed at the Republic's expense; dogs guard the hill at night, for thieves | The goose-keeper, `rome.anser.move.1`, `.feed.1`, `.chickens.1`, `.dogs.1` | **Checked.** P&A, "Area Capitolina"; Cicero, *Pro Sexto Roscio Amerino* 56 (Yonge) |
| Long ago the Gauls took the city, all but the Capitol; they climbed it by night so quietly that not even the dogs woke; Juno's geese woke Manlius with their cries and their wings; he knocked the first Gaul down, and the rest fell back | The goose-keeper, `rome.anser.tale.1` to `.5` | **Checked.** Livy 5.47 (Roberts; Perseus, read again 13 October); Wikipedia, "Sack of Rome (390 BC)", read 13 October ("with the exception of the Capitoline Hill"). Rome's own history, part legend, told as his story; no year is said |
| The geese cannot abide anything strange: they shout at it, and then they run | The goose-keeper, `rome.anser.tale.6`; Walnut, `rome.urchin.tip.geese` | The game's own, built on the story (the geese raise the alarm in Livy; that they then run is the puzzle's) |
| Anser means "goose" | The goose-keeper, `rome.anser.name.1` | **Checked.** Lewis & Short |
| Every Ides a white ewe goes up to Jupiter | The keeper, `rome.keeper.errand.ewe`; Titus, `rome.titus.who.2`, `.ewe.1` | **Checked.** Festus (in Lewis & Short, "idulis"); Ovid, *Fasti* 1.56. Her ribbons (`rome.titus.ewe.2`): Probable. Nobody says how she was offered |
| Statues of the kings stand on the Capitol, one (Brutus) with a drawn sword, with writing on his base | The Son, `rome.capitol.kings.look`, `rome.capitol.brutus.look` | **Checked.** Plutarch, *Brutus* 1; Suetonius, *Julius* 80.3. What was written is not said |
| The dictator's statue stands among the kings; his chariot faces the temple; another statue of him stands on a figure of the world | The Son, `rome.capitol.dictator.look`, `.chariot.look`, `.world.look` | **Checked.** Dio 43.45.3, 43.14.6 (Cary). The world as a ball is the picture's: Probable. The word "demigod" is not said |
| Bronze tablets of decrees on the Capitol | The Son, `rome.capitol.tablets.look` | **Checked.** Josephus, *Antiquities* 14.188, 14.197 (Whiston). How they were mounted is the picture's |
| The hut of Romulus, thatched, in the precinct | The Son, `rome.capitol.hut.look` | **Checked.** P&A, "Area Capitolina"; Vitruvius 2.1.5, read 13 October (the house of Romulus on the Capitol, "by its thatched roof"). Round: the picture's |
| Pompey's stone theater on the plain, with a temple at the top of its seats | The Son, `rome.capitol.theater.look`; the Gaul, `rome.gaul.pompey` | **Checked.** P&A, "Theatrum Pompei" |
| The island and its temple; the bridges | The Son, `rome.capitol.view.look` | **Checked.** Wikipedia, "Tiber Island"; P&A, "Pons Aemilius" (close to the Sublicius) |
| The Janiculum, a hill across the river | The Son, `rome.capitol.janiculum.look` | **Checked (secondary).** Wikipedia, "Janiculum", read 13 October. Its pines are the picture's |
| The Senate meets today in Pompey's hall | The boy, the Gaul and Walnut, `rome.gaul.opt.pompey`, `rome.urchin.tip.gaul` | **Checked.** The row above. "They cannot meet in a hole" is the Gaul's own reasoning (the sources give no reason: Probable as his) |
| The dictator has made Gauls senators, and the city sings of Gauls who put off their trousers for the broad stripe | The Gaul, `rome.gaul.who.1`, `.song.2`; the senator, `rome.senator.wrong.6` | **Checked.** Suetonius, *Julius* 76.3, 80.2. The verses are never quoted |
| A notice was put up that nobody is to show a new senator the way to the House | The Gaul, `rome.gaul.who.3` | **Checked.** Suetonius, *Julius* 80.2 (Rolfe: a placard) |
| Nine hundred senators | The Gaul, `rome.gaul.caesar.1` | **Checked.** Dio 43.47.3 (Cary) |
| Gaius Iulius Litumarus, of Nemausus in the Province | The Gaul, `rome.gaul.who.1` | Litumaros, a Gaulish name: **Checked (secondary)** (Lambert, as listed by S. Gabriel). Nemausus in the Province: **Checked (secondary)**, Wikipedia, "Gallia Narbonensis" ("simply Provincia ('the Province')") and "Nimes" (the Volcae Arecomici's town, in the province from 121 B.C.), read 13 October. A new citizen taking the dictator's names: Probable |
| Gaulish men of rank wear moustaches, and Romans shave | The Gaul, `rome.gaul.mustache.1` | **Checked** (Diodorus 5.28.3, Oldfather); Romans clean-shaven: Probable |
| A senator's toga is plain white | The Son, `rome.senator.toga.1` (decision 12) | **Checked.** Wikipedia, "Toga" |
| The Tuscan street leads from the Forum toward the cattle market and the stone bridge | The Son, Phyllis and Walnut, `rome.forum.tuscan.look`, `rome.phyllis.take.1`, `rome.urchin.tip.felix` | **Checked (secondary).** Wikipedia, "Vicus Tuscus", read 13 October; P&A, "Pons Aemilius" (it crossed from the Forum Boarium) |
| Caesar's gardens along the river road on the far bank | The Son, `rome.tiber.road.look`, `rome.tiber.gardens.look` | **Checked.** P&A, "Horti Caesaris". Nobody says whose they are |
| Jews live across the Tiber, many of them captives brought to Italy and freed by their owners, with houses of prayer | Eleazar, `rome.eleazar.rome.1` to `.3`; the date seller, `rome.dateseller.eleazar`; the Son, `rome.tiber.prayerhouse.look` | **Checked** for Philo's day (*On the Embassy to Gaius* 155-156, Yonge); for 44 B.C.: Probable |
| Pompey took Jerusalem nineteen years ago, and many Jews were brought to Rome | Eleazar, `rome.eleazar.rome.1` | **Checked.** facts-home (`rome.pompey.temple`): 63 less 44 is 19 |
| He prays toward the Temple in Jerusalem, evening, morning and midday | Eleazar, `rome.eleazar.window.1` | **Checked** as Scripture's custom (Daniel 6:10; Psalm 55:17); for a Jew of Rome in 44 B.C.: Probable |
| Words of the Law on the doorposts | Mariam, `rome.mariam.doorpost.1`; the Son, `rome.tiber.doorpost.look` | **Checked** (Deuteronomy 6:9); on a door in Rome in 44 B.C.: Probable |
| Tassels with blue on the corners of the mantle, worn so as to remember | Eleazar, `rome.eleazar.tassels.1` | **Checked.** Numbers 15:38-39, Bible Hub, read 13 October |
| Her father sells dates from Jericho | Mariam, `rome.mariam.family.1` | **Checked.** The row above (Jericho's dates) |
| Paul lives in Corinth one day and makes tents; he wrote two letters to it | The Son, `rome.felix.paul.son.1` | **Checked.** Acts 18:1, 18:3, 18:11 (Bibleserver, read 13 October); 1 and 2 Corinthians |
| Daniel prayed with his windows open toward Jerusalem three times a day; the lions' story | The Son, `rome.eleazar.window.son`, `rome.tiber.arrive.2` | **Checked.** Daniel 6:10, 6:16 (Bibleserver, read 13 October) |
| He prays for Jerusalem's peace, and for a son of David, a king who will rule in righteousness, whose kingdom will have no end; the nations will come to his light | Eleazar, `rome.eleazar.prayfor.1`, `.2` | **Checked**, as told: Psalm 122:6; Isaiah 9:7; Isaiah 32:1; Isaiah 60:3, with 11:10 and 49:6 (Bible Hub and Bibleserver, read 13 October). In 60:3 the light is Zion's; "his light" is the design's telling of the three together |
| **QUOTED:** Isaiah 40:31, Numbers 6:25 and 6:26 | Eleazar and the boy | **Checked**, exact: the Scripture table above |
| Mariam's hens stand facing the city and will not eat | Mariam; the Son | The author's rule (`briefs/DATING.md`). Not history, and nobody says it is |

Sources read on 13 October for this table, beyond the design's: Bible Hub, King James
Version: [Isaiah 40](https://biblehub.com/kjv/isaiah/40.htm), [Isaiah 11](https://biblehub.com/kjv/isaiah/11.htm),
[Isaiah 32](https://biblehub.com/kjv/isaiah/32.htm), [Numbers 6](https://biblehub.com/kjv/numbers/6.htm),
[Numbers 15](https://biblehub.com/kjv/numbers/15.htm); Bibleserver, King James Version:
[Isaiah 40](https://www.bibleserver.com/KJV/Isaiah40), [Isaiah 9](https://www.bibleserver.com/KJV/Isaiah9),
[Isaiah 49](https://www.bibleserver.com/KJV/Isaiah49), [Numbers 6](https://www.bibleserver.com/KJV/Numbers6),
[Psalm 122](https://www.bibleserver.com/KJV/Psalm122), [Daniel 6](https://www.bibleserver.com/KJV/Daniel6),
[Acts 18](https://www.bibleserver.com/KJV/Acts18); Livy 5.47 on
[Perseus](https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.02.0026%3Abook%3D5%3Achapter%3D47);
Vitruvius, book 2, on [LacusCurtius](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Vitruvius/2*.html);
Wikipedia: [Vicus Tuscus](https://en.wikipedia.org/wiki/Vicus_Tuscus),
[Roman timekeeping](https://en.wikipedia.org/wiki/Roman_timekeeping),
[Ancient Corinth](https://en.wikipedia.org/wiki/Ancient_Corinth),
[Sack of Rome (390 BC)](https://en.wikipedia.org/wiki/Sack_of_Rome_(390_BC)),
[Basilica Aemilia](https://en.wikipedia.org/wiki/Basilica_Aemilia),
[Treadwheel crane](https://en.wikipedia.org/wiki/Treadwheel_crane),
[Janiculum](https://en.wikipedia.org/wiki/Janiculum),
[Gallia Narbonensis](https://en.wikipedia.org/wiki/Gallia_Narbonensis),
[Nimes](https://en.wikipedia.org/wiki/N%C3%AEmes),
[Religion in ancient Rome](https://en.wikipedia.org/wiki/Religion_in_ancient_Rome).

**What the Son gets wrong out loud, on purpose.** Togas are bedsheets. The sacred
chickens are pets. The temple is a church and a bank. The jars in the counter hold
soup. The walnut game is marbles. MARCVS is misspelled, and VOTA might mean vote. The god
has a blanket on his head and a hook knife. Dates are giant raisins, and the stone in
one is a rock. No Roman agrees with any of it. About the Bible he is not wrong: what he
tells, he tells in a ten-year-old's words, and he gets it right.

Since round thirteen: the Gaul is a Viking; the sacred geese are attack chickens; the house
of prayer is a church; the basilica of Paullus is a mall; the barge is a table that floats;
the altar on the Capitol is a barbecue the size of a minivan; the case on the doorpost is a
doorbell that does not ring; the old man's mantle is a blanket with strings. Nobody of the
time agrees: "I do not know that word. I am a Gaul."; "They are the sacred geese of Juno,
child."; "A house of prayer."; "It's a barge."; "Not a blanket, child, and not strings."

**What nobody says.** Nobody on screen knows what will happen to Caesar today, and the
game neither shows it nor says it. The soothsayer does not know why the day is bad. The
senator hurries off to an ordinary meeting. The keeper knows Caesar as a nose on a coin.
The date seller calls him a friend to the Jews of Rome, and does not know that it is
the last morning he will be one. Nobody in Rome knows who Gaius Octavius will be, or
Herod. The boy knows, and each time says only "Not yet.", or less. Nobody tells the date
seller what is coming, or when: the boy does not know the number of years himself. No
line says how long before or after anything in the Old Testament this morning is: none
needs to, and if one ever does, the count is the Bible's (`briefs/DATING.md`). Nobody
explains the chickens.

Since round thirteen: nobody in the Forum, on the Capitol or across the river knows what will
happen in Pompey's hall today; the Gaul goes to an ordinary meeting, and Felix's ninth hour is
only a promise to his mother. Nobody says how the Ides ewe went up. The goose-keeper says "long
ago", and no year. Nobody in this stage speaks of the queen across the river. Nobody explains
Mariam's hens.

**One fact outside this act that these sources bear on.** Big Sister used to say in Act
Four (`nevada.coin.read.2`) that Caesar "was the first living Roman to put his own face on
Rome's coins". The Roman currency page says the opposite: "living Romans had appeared on
coinage before", and that Caesar's portrait "marked the third instance in Roman history
where a living individual was depicted". Her line was reworded on 7 October, and says only
that in 44 B.C. coins were struck in Rome with Caesar's own portrait, while he was alive
(Checked, in CHARACTERS.md).

---

## What comes next (not written)

- The Son is still in the temple. The door is open, the size of a coin, and he has
  nothing left to send through it. Something could come back the other way. (Round
  twelve: in Act Four his family speaks into the Nevada end of it and he answers, and
  Little Sister posts a penny through it for him, which waits in the tunnel for this end.)
- The tunic has to go back clean, and Walnut is owed two nuts.
- Whether Dad's door in Egypt, opened as wide as a whole sun, comes out here.
<!-- ROME-13W: what waits after the bigger Rome's first stage (briefs/ROME-13.md, "What waits for a later stage") -->
- **Caesar's house** (`rome-house`, off the Forum's bottom edge), with its porter Anteros,
  the callers, the lictors and their rods, the litter and its bearers, the maid Doris and her
  whispers, and the design's Nine Hundred Senators: it needs the senator at Caesar's door
  (decision 1, held until the author has played this stage). With it, the keeper's knowing
  the senator's three names, and the senator's lines at the door.
- **The optional speakers**: Diodorus, the Capitol's guide (Catulus the puppy, old Brutus,
  the dictator's statues, the decree for the Jews on bronze, the view, the queen as gossip);
  Paetus the moneychanger (coins, Moneta, debts, the rumor about Cotta); Demetrius (the
  calendar, July); Vibius (the senate house going up, the speakers' platform, the diadem);
  Petosiris (papyrus, Egypt's year, the queen as gossip). Their places are painted now and
  left clear.
- **People without lines**: the revellers going to Anna Perenna's feast, the nurse and child,
  the builders, the tutor and his boy, the woman at the well.
- **Titus at his father's counter** once he is home (in this stage he is simply gone home).
- **The act's old conversations rewritten as trees**, after the author's review of the puzzles.
- **The Rome end of the letterbox** (the penny, the Son hearing his sisters), with Round One's step.
- **The A.D. chapter** (`briefs/out/ad-way-plan.md`).

What the builders of round thirteen chose where the design left them a choice, or could not
build it as written (the senator's empty hand, the goose-keeper behind his pen, the Son
standing to wait, Juno Moneta not painted on the Capitol, and the rest), each with what the
game does meanwhile, is listed for the author in [DESIGN.md](DESIGN.md), section 14, "Decisions
waiting for you".
