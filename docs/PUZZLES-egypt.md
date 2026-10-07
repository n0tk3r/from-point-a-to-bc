# Act One: Egypt, about 2560 B.C.: puzzle document

The first act of the game, played as Dad. The wagon has come down by the Nile while the
Great Pyramid is being finished. His son got here first, went inside to look, and was
taken by a door in the air. Dad follows the sneaker prints, talks his way in, works out
how the door opens, and opens it wide.

It is laid out the way [PUZZLES-the-present.md](PUZZLES-the-present.md) is: the people,
the puzzle structure, the places, and then the cut-scenes and puzzles in order, each
with its setup, its solution, what it teaches and its hints. After that come the
ledger, the places where the scripts differ from the design, what happened to the old
act's lines, and a table of every historical statement the act makes.

**Status: it plays, from the arrival to the hand-over to Rome.** The four scenes are
laid out on the painted pictures from the painters' own measurements
(`art/scenes/<scene>/layout.json`); no number in them is a guess any longer. Two
scripts check the act (see "How it was checked"): one reads the files and dry-runs
them, the other plays the act in the real game by real mouse clicks, two ways through.
Two figures were still being drawn when this was written, the guard with his arms up
to hold the shade and the goldsmith in the sunglasses. Until they exist those two men
look as they always do; the scenes take up the new figures by themselves when they
arrive (see "Not done").

Play it: a new game starts here. `index.html?scene=egypt-crash&lead=dad` starts the act
directly; the other three scenes are `egypt-site`, `egypt-gallery` and `egypt-chamber`,
and each scene file gives the `&flags=` to start it at a later moment.

## The idea of the act

**A door in time stays where it once opened, shut and invisible, and it hums. Light
thrown on the place opens it, and the more light, the bigger the door.** Nobody in the
past knows this. They know what they saw. The player works it out, in three steps:

1. **Somebody saw it** (the lamp boy): a small one pointed "a little sun" at the wall,
   and the wall opened.
2. **Dad tries it** (the flashlight): a hole the size of a dinner plate, which he is
   not. Then the batteries die, and he says the rule out loud.
3. **Dad scales it up** (three reflectors): there is a whole sun going to waste
   outside. A windshield shade, a door mirror and a goldsmith's copper mirror bring it
   around three corners to the wall, and the player watches the beam grow a stretch at
   a time.

Everything he needs came with him, on the roof rack of the family wagon. That is the
other idea of the act: **Dad makes tools out of what is in the car, and talks his way
around people.**

Nobody in this act is stupid and nobody is mocked. The Egyptians are entirely serious
about their own world: a list, a schedule, a guard duty, a lamp to fill. Dad treats
2560 B.C. as a rest stop with poor signage. He shortens his words; they never do.

## Characters

- DAD: the driver of the shortcut; unshakeably confident, wrong about small things, right about people; wants his son back, and for it never to come up that he was lost.
- WATER CARRIER (`carrier`, by the river with Donkey): old, slow, has seen everything and is impressed by none of it; saw the boy go up the track asking for the "wy-fy"; wants a slow day.
- SCRIBE (`scribe`, under his awning at the site): keeps the lists; nothing exists until he has written it down, and his pen has split; wants a pen, and then something to write on.
- OVERSEER (`overseer`, the site): loud, harassed, behind schedule for the first time in twenty years; takes Dad for a specialist somebody sent for; wants the wall to stop humming, today.
- HAULERS (`hauler1`, `hauler2`, `hauler3`, the site): the gang "Friends of Khufu"; one speaks, one agrees, one eats; paid in bread and beer and proud of it; want their break to go on.
- GUARD (`guard`, the foot of the stair): tall, bored, very hot; guards, and does not hold; wants something cold, and believes there is no such thing.
- LAMP BOY (`lampboy`, the foot of the gallery): twelve; fills every lamp from here to the top, except today; the only one who saw; wants never to go up there again.
- GOLDSMITH (`goldsmith`, the burial chamber): very old, cheerful, deaf from fifty years of hammering, so the hum does not trouble him; mishears everything; his eyes are tired of shining things; wants never to see his own mirror again.

## Puzzle structure

```
                   Cut-scene: Crash landing by the Nile
                                   |
                 +-----------------+------------------+
                 |                                    |
         #1 The Road Map                        #2 A Reed
         (the glovebox)                         (the reed bed)
                 |                                    |
                 |                         #3 A Pen For The Scribe
                 |                                    |
                 +-----------------+------------------+
                                   |
                           #4 A Pass                              chain A: getting inside
                                   |
                           #5 Past The Guard
                                   |
                 +-----------------+------------------+
                 |                                    |
         #6 The Witness                  (the flashlight: in the trunk,
         (the lamp boy)                   to be had at any time)
                 |                                    |
                 +-----------------+------------------+
                                   |
                           #7 The Flashlight                      chain B: the rule
                                   |
         +-------------------------+-------------------------+
         |                         |                         |
  #8 The Shade             #9 The Door Mirror         #10 The Trade
  (trunk and cooler;       (the wagon's door;         (the suitcase;
   the guard holds it)      the slot at the foot)      the goldsmith)
         |                         |                         |
         |                         |                 #11 The Copper Mirror
         |                         |                 (the step at the top)
         |                         |                         |
         +-------------------------+-------------------------+
                                   |
                           #12 The Door                           the gate
                                   |
          Cut-scene: Meanwhile, about twenty-five hundred years later
```

Goal of the act: **follow the boy through the door.** Chain A is one chain with two
loose ends at the start (the map and the reed can be picked up in either order, and
before he knows why). Chain B is short and is the turn of the act. Chain C is three
jobs in any order, and whichever is done last completes the beam.

#6 is not strictly needed for #7: a player who shines the flashlight at the humming
wall without talking to the lamp boy is rewarded for it (see "Where the scripts differ").

## Location layout

```
+--------------------------------------------------------------------------+
| 1. WHERE THE WAGON CAME DOWN  (egypt-crash)                              |
|                                                                          |
|  the Nile    palms      the PYRAMIDS, far off        a dropped block     |
|  a boat      REEDS      the far end of the TRACK  -> to 2                |
|                         SNEAKER PRINTS going up it                       |
|  WATER CARRIER and Donkey                                                |
|                         THE WAGON: hood (steaming), GLOVEBOX, DOOR       |
|                         MIRROR; on the roof SUITCASE, TRUNK, COOLER      |
+--------------------------------------------------------------------------+
| 2. AT THE FOOT OF THE PYRAMID  (egypt-site)                              |
|                                                                          |
|  small pyramids,        the pyramid's shaded face, its scaffold, and     |
|  the stone yard         the ENTRANCE up a STAIR  -> to 3                 |
|  SCRIBE under his       HAULERS by the rope      GUARD at its foot       |
|  awning, the day's      the SLEDGE and its block, the OVERSEER before it |
|  wages beside him       the SUNNY SPOT           masons' tools           |
|  <- the track to 1 (past the water jars)                                 |
+--------------------------------------------------------------------------+
| 3. THE GREAT GALLERY  (egypt-gallery)                                    |
|                                                                          |
|                 the DOORWAY AT THE TOP  -> to 4                          |
|                 the TOP STEP                                             |
|                 the ramp, lamps all the way up     builders' marks       |
|  <- the WAY OUT to 2    a low passage (dark)       the SLOT at the foot  |
|  a ladder, oil jars                                LAMP BOY on the bench |
+--------------------------------------------------------------------------+
| 4. THE BURIAL CHAMBER  (egypt-chamber)                                   |
|                                                                          |
|  bare granite walls     THE KING'S FURNITURE       THE WALL THAT HUMS    |
|  <- the doorway to 3    (gold bed, chairs, chests) (later: THE DOOR)     |
|                         GOLDSMITH behind his       the sarcophagus,      |
|                         bench, his COPPER MIRROR   its lid on the wall   |
+--------------------------------------------------------------------------+
```

Four places in a row: river, site, gallery, chamber. There is no map and no shortcut.
The player walks the row several times, and it is short.

The sunbeam, when it is whole, runs through three of them: sun, shade (2), up the stair
and in at the entrance, across the foot of the gallery to the door mirror (3), up the
ramp to the copper mirror on the top step, in at the doorway, across the chamber and
onto the wall (4).

## Cut-scenes and puzzles

```
Cut-Scene: Crash landing by the Nile        (opens the act)
```
The wagon, nose-down in the sand, steaming. "Okay. Nobody panic. The car has landed."
"Buddy? ... Buddy?" He was in the passenger seat a minute ago, or a thousand years from
now. Then Dad sees them: small sneaker prints, going up the track toward the pyramid.
"He's gone to see the biggest thing in sight. I'd be annoyed if I hadn't taught him that."
*Plants:* the prints (the boy went up, and in). That the car is all Dad has.

```
Puzzle #1: The Road Map        (Egypt · Lead: Dad · the wagon's glovebox)
Needs:        nothing
Setup:        The wagon is the one familiar thing in sight, and it is full of his own stuff.
Wrong tries:  The wagon itself       -> "I turned the key. She made the noise she makes when I bring
                                        up the transmission."
              The hood               -> "She's just thinking it over."
              The door mirror        -> "I'm not taking my own car apart without a reason. I usually
                                        have at least a bad one."
Solution:     Search the glovebox. "There's a road map in the glovebox. Three states, zero centuries."
Gives:        The road map.
Teaches:      That the car is a store of things, and each part of it is its own thing to click.
              The player who opens everything now has the flashlight, a root beer and the sunglasses
              before they know what any of them is for.
Hints:        Hint button: "I should check what's still in the wagon."
Plants/pays:  The ketchup packets he is saving. The shade and the mirror that he will not take yet.
Notes:        Afterwards: "Nothing left in there but ketchup packets. I'm saving those."
```

```
Puzzle #2: A Reed        (Egypt · Lead: Dad · the reed bed)
Needs:        nothing
Setup:        "Reeds. Nature's ballpoint."
Wrong tries:  A second reed          -> "One is plenty. I'm not opening a stationery shop."
Solution:     Pick one. "One reed. I'll bring it back. That's a lie. I never bring pens back."
Gives:        The reed.
Teaches:      That things in the landscape can be taken, not only things in the car.
Hints:        Said in the world: the water carrier, asked for news, says the scribe's pen has
              split; the scribe says so himself.
              Hint button: "The scribe's pen has split. Something by the river might do for a new one."
Notes:        It can be cut before he has met anybody, as in the old act.
```

```
Puzzle #3: A Pen For The Scribe        (Egypt · Lead: Dad · the scribe's station)
Needs:        #2
Setup:        The guard lets nobody up who is not on the scribe's list, and the scribe can put
              nobody on it: his pen split at dawn. "Since then nothing has happened here. Not
              officially."
Wrong tries:  The map first          -> "A fine sheet. I have nothing to mark it with." (He gives it back.)
              A root beer            -> "Beer made of roots. I will not enter that. The brewers would
                                        never forgive me."
Solution:     Give him the reed. "Here. It's a pen. Some assembly required." "A good reed. You have the
              eye of a scribe and the clothes of a market stall." "A rush is the proper thing for a
              pen. But a man without one cannot be particular." "You have delivered one reed. That
              makes you a supplier. Suppliers go on the list."
Gives:        A scribe who can write. A reason to be on the list.
Teaches:      Using a carried thing with a person.
Hints:        Said in the world: the guard ("Then walk to the scribe. Under the awning."), the
              overseer ("Get onto the scribe's list."), the scribe ("I write him onto it. With a pen.
              You see the difficulty.").
              Hint button: "I have a reed, and I know a man who needs a pen."
Plants/pays:  Pays off the water carrier's news. Plants the next want at once: "But the guard wants
              a pass, and my last clean sheet is for the grain account."
```

```
Puzzle #4: A Pass        (Egypt · Lead: Dad · the scribe's station)
Needs:        #1 and #3
Setup:        He has a pen and nothing to write a pass on.
Wrong tries:  Ask about the list     -> "I write him a pass. On a sheet. My last clean sheet is for
                                        the grain account."
Solution:     Give him the road map. "Draw on this. It's a map. It's already wrong, you can't make it
              worse." He writes on the back: "'One supplier of reeds. Foreign. Loud about the
              shoulders.' There. Now you exist."
Gives:        The work pass, in place of the map. "A hall pass. Thirty years out of school and I've
              finally got one."
Teaches:      That the order of things matters (pen, then sheet), and that one thing can become another.
Hints:        Said in the world: the scribe, at the end of #3 and whenever he is asked about the list.
              Hint button: "The scribe wants something to draw on. A map is mostly drawing."
Notes:        Dad calls writing "drawing" throughout. To him it is.
```

```
Puzzle #5: Past The Guard        (Egypt · Lead: Dad · the stair)
Needs:        #4
Setup:        The entrance is up a stair on the shaded face. "Nobody goes up who is not on the
              scribe's list."
Wrong tries:  The stair, with no pass -> the line above. "I'm more of a walk-in." "Then walk to the
                                        scribe. Under the awning."
              The road map           -> "That is not the scribe's hand. That is a great many roads to
                                        nowhere I know."
Solution:     Show the pass: click the entrance, the stair or the guard with the pass in his pockets,
              or use the pass on any of them. "The scribe's hand. I know it. It looks like geese in a
              quarrel. You are on the list. Go up. If it hums at you, do not bring it down here."
Gives:        The inside of the pyramid, from now on. (He keeps the pass.)
Teaches:      That a way through can belong to a person.
Hints:        Hint button: "I'm on the list, and I've got the pass to prove it. The guard at the stairs
              ought to see it."
Notes:        The stair is not walked by clicking on it: the entrance, the stair or the guard takes
              him up it, along the painter's marks for his feet. The whole climb is shown the first
              time. It is a long stair, so after that the picture changes when he is a few steps
              up, and when he comes out again he is found halfway down.
```

```
Puzzle #6: The Witness        (Egypt · Lead: Dad · the foot of the gallery)
Needs:        #5
Setup:        Everybody outside has told him the same thing: no boy on the list, a boy who rode the
              sledge, a wall that hums. One person saw more, and he is sitting as far from the top of
              the gallery as the gallery allows.
Wrong tries:  The flashlight, shown to him -> "No. Keep your sun in your own hand. I saw what the
                                        small one's did." (Which is the same clue.)
Solution:     Ask him about the boy. "I saw him. I am the only one who saw. A small one came, with a
              little sun in his hand. He pointed it at the wall and the wall opened like an eye and it
              took him." Dad: "A little sun in his hand. That's the flashlight off his key ring. So it
              opens for a light. I've got a light. A bigger one."
Gives:        The clue: light did it. Dad says where his own light is (in the trunk, or in his pocket).
Teaches:      That the people of the past only know what they saw, and the player has to read it.
Hints:        Said in the world: the overseer ("Ask the lamp boy. He saw something, and he tells me
              nothing.").
              Hint button: "Somebody in that pyramid saw what happened. The boy with the lamps has the
              look of a witness."
Plants/pays:  "It is not a door. I know every door in the Horizon. I light them. This opened where the
              masons put nothing."
```

```
Puzzle #7: The Flashlight        (Egypt · Lead: Dad · the burial chamber)
Needs:        #5, and the flashlight from the trunk (which can be taken at any time)
Setup:        "Bare wall, empty air, a clean ring swept on the floor. And a hum. Probably the wind."
              The old goldsmith works on beside it: "WHAT HUM?"
Wrong tries:  Touch it                -> "I knocked on the air. It's like knocking on a door from the
                                         wrong side. Nobody came."
              The flashlight on the goldsmith -> "Put it OUT. I have enough bright in here."
              The flashlight down the low passage in the gallery -> "It goes a long way into nothing.
                                         The batteries didn't enjoy it."
Solution:     Shine the flashlight at the place that hums. A round hole opens in the air, just past
              his hand. "A hole in the air the size of a dinner
              plate. I am not the size of a dinner plate." He steps closer: "It shrinks every time I get
              close. I have the same effect on waiters." The batteries die and the hole goes with them.
              "So that's the trick. Light opens it. A little light, a little door. More light, more
              door. And there's a whole sun going to waste outside."
Gives:        The rule ("egypt.knowsLight"). From now on Dad will take the windshield shade out of the
              trunk and the mirror off the door.
Teaches:      The rule of every door in the game.
Hints:        Said in the world: the lamp boy (#6); the overseer, once Dad has heard the boy ("Then find
              a little sun. I have only the big one.").
              Hint button: "A little sun in his hand: a flashlight. I packed one of those. And the wall
              that hums is at the top of the gallery."
Plants/pays:  Pays off #6, and the flashlight he packed "in case of a flat". Keeps the old act's two
              best lines exactly.
Notes:        The dead flashlight stays in his pockets ("Dead. I've shaken it. Shaking is all I know
              about batteries."). The lamp boy will take it off him: "It is a lamp. Lamps I understand.
              I will fill it."
```

```
Puzzle #8: The Shade        (Egypt · Lead: Dad · the wagon, then the sunny spot at the site)
Needs:        #7
Setup:        There is a patch of sand at the site in full sun, with a clear line up to the entrance.
              "If light were a golf ball, this is the tee." The windshield shade is in the trunk.
Wrong tries:  The shade, held up there by Dad -> the beam leaps up into the doorway. "And it stops when
                                         I let go. I can't stand out here and be in there. I need a
                                         volunteer."
              Ask the guard           -> "I guard. I do not hold. I would hold it for something cold. There
                                         is nothing cold. So I guard."
              Ask the haulers         -> "We pull. Holding is another trade." "A lesser trade."
              Ask the overseer        -> "I oversee. If I stand there holding that, who oversees me
                                         holding it?"
              Ask the scribe          -> "I hold a pen. It is all I hold. Ask a man with idle arms."
Solution:     Bring the guard a root beer from the cooler. "It bites the tongue. Like a small friendly
              snake." He takes the shade to the sunny spot. "For how long?" "Not long." "The overseer
              says 'not long'. He has said it for twenty years." And the sunbeam goes "up the stairs and
              in through the door, and nobody asked it for a pass".
Gives:        The first stretch of the beam: from the site into the gallery, as far as the foot of the ramp.
Teaches:      That a job can be somebody else's, at a price, and that the price is in another place.
Hints:        Said in the world: Dad at the sunny spot ("I need a volunteer."); the guard ("I would hold it for
              something cold."); Dad, looking back down the track ("...the only cold drinks in Egypt.").
              Hint button: "The windshield shade could throw the sun into that doorway, if somebody held
              it. The guard looks thirsty."
Plants/pays:  Pays off the cooler. The guard complains of his arms for the rest of the act.
Notes:        No dead end: a guard who is given a root beer before there is a shade to hold says "I owe
              you one holding. Of anything. Not heavy.", and pays it later. The cooler always has one more.
              The guard walks round the sledge to the sunny spot. Holding the shade he is the figure
              `guard-shade` (the same man, arms raised), with the painted shade in his hands.
```

```
Puzzle #9: The Door Mirror        (Egypt · Lead: Dad · the wagon, then the foot of the gallery)
Needs:        #7
Setup:        Once the shade is up, the sunbeam comes in at the passage and lands on a slot in the stone
              bench at the foot of the ramp. "Stone's a poor mirror. I checked."
Wrong tries:  The copper mirror in the slot -> "It won't wedge. It wants a flat place to stand, like the
                                         rest of us."
              The shade in the gallery -> "No sun in here to bounce. That's the whole problem."
Solution:     Twist the door mirror off the wagon ("It's been one twist from off since March") and wedge
              it in the slot. "Wedged. That's not coming out. Nothing I wedge ever does."
Gives:        The second stretch of the beam: up the ramp to the top step.
Teaches:      That the car can be taken apart, given a reason. That a thing can be put down in the world.
Hints:        Said in the world: Dad, on seeing the beam stop at the bench; looking at the slot.
              Hint button: "The sunbeam has to turn at the foot of the gallery. The car has a mirror it
              isn't using."
Notes:        Done before the shade is up: "A mirror with nothing to reflect. I've worked with people
              like that."
```

```
Puzzle #10: The Trade        (Egypt · Lead: Dad · the wagon, then the burial chamber)
Needs:        #7 (see "Where the scripts differ": the goldsmith does not make him wait)
Setup:        The goldsmith owns a polished copper hand mirror and cannot stand the sight of it. "Fifty
              years of gold, all of it shining at me. I am tired of shining things. That mirror most of
              all. It shines AND it shows me my face."
Wrong tries:  Ask to borrow it        -> "MY SORROW? Yes. That mirror. I check the gold in it, and it
                                         checks my face. Leave it be."
              A root beer             -> "GOOD BEER? ... No. Somebody has played a trick on beer."
              The door mirror         -> "ANOTHER mirror? Is this a joke? Who sent you?"
Solution:     Give him the sunglasses from the suitcase. "Oh. ... Oh, that is kind. The whole world has
              gone the color of good beer. I never want to see a shining thing again. That mirror least
              of all. Take it. Take it away."
Gives:        The copper mirror.
Teaches:      That the way to a thing is somebody's trouble, and that being kind is a move.
Hints:        Said in the world: the goldsmith, asked about his eyes; Dad's answer ("Tired eyes and too
              much glare. I packed a thing for that.").
              Hint button: "The goldsmith has a mirror, and eyes that are tired of shining things. I
              packed sunglasses."
Plants/pays:  Pays off the suitcase. From now on: "I wear the night on my nose now. Nothing shines at me
              in there."
Notes:        He puts them on at once, and from then on he is the figure `goldsmith-shades` (the same
              man, in the sunglasses), whenever the chamber is shown.
```

```
Puzzle #11: The Copper Mirror        (Egypt · Lead: Dad · the top of the gallery)
Needs:        #10 and #7
Setup:        At the top of the ramp there is a tall step, flat as a table, right in front of the low
              doorway to the chamber.
Wrong tries:  The door mirror on the step -> "It won't stand up on its own. It was built to hang off a
                                         door."
              Before #7                -> "A mirror at the top of a dark ramp. I'd only be decorating."
Solution:     Stand the copper mirror on the step. "There. Tilted at the little door. He kept it
              polished, I'll give him that."
Gives:        The last stretch of the beam: in at the doorway, across the chamber, onto the wall.
Teaches:      That the three jobs can be done in any order, and the game keeps up.
Hints:        Hint button: "The copper mirror belongs on the step at the top of the gallery, to turn the
              light into the chamber."
Notes:        Done before the beam reaches it: "It's reflecting the dark beautifully. The daylight
              hasn't made it this far up."
```

```
Puzzle #12: The Door        (Egypt · Lead: Dad · the burial chamber)        THE GATE
Needs:        #8, #9 and #11
Setup:        Whichever reflector goes in last, Dad says the beam is through ("That's the whole relay",
              or "that's going all the way in"). The next time he walks into the chamber, he steps
              out of the doorway, the sunbeam comes in behind him and crosses to the wall, and the
              door opens: round at first, then stretching to a tall oval that stands on the floor
              and fills the bare piece of wall. "Now that's a door." The goldsmith: "Somebody
              has let the day in. Let it look. I am wearing the night."
Solution:     Go through it. "Hold on, buddy. Dad's taking the next shortcut."
Gives:        The end of the act.
Hints:        Hint button: "The door is holding still now. Time to go through it."
Notes:        If the player later switches back to Dad, he is still there: "Not until I know where it
              comes out. I've made that mistake once today."
```

```
Cut-Scene: Meanwhile        (closes the act)
```
The picture fades on Dad at the door. A card: "Meanwhile", "about twenty-five hundred
years later". The time tunnel, and the story is the Son's, on the steps of a temple in
Rome (`rome-steps`, Act Two).

Also in the act, for character and nothing else: the river, the boat of white stone,
the palms, the dropped block, Donkey, the hood, the six loud shirts, the lawn chair and
the jumper cables; at the site the pyramid, its scaffold, the small pyramids, the stone
yard, the scribe's station, the sledge, the hauling rope, the mud bricks, the water
jars and the masons' tools; in the gallery the walls, the low passage, the builders'
marks, the oil jars, a ladder, a coil of rope, a worn sled runner, a chest somebody set
down halfway up and somebody's bread and beer; in the chamber the bare walls, the
king's furniture, the sarcophagus and its lid, the goldsmith's bench and his brazier.
Everything the painters put in a picture and listed in its `layout.json` has a line.
Thirteen of them have a second thing to say when looked at again.

Dad asks six people the same question, in the same words: "Have you seen a boy? About
this tall, asks a lot of questions?" Each answer is a different piece of where the boy
went: up the track, not on the list, on the sledge, into the wall.

## Ledger

**Things that are carried** (all Dad's)

| Thing | Comes from | When | Used for |
| --- | --- | --- | --- |
| `reed` reed | the reed bed, scene 1 | any time | #3: the scribe's new pen |
| `map` road map | the glovebox, scene 1 | any time | #4: the scribe writes on the back of it |
| `pass` work pass | the scribe, in place of the map | #4 | #5: gets Dad past the guard; kept |
| `flashlight` flashlight | the trunk, scene 1 | any time | #7: opens a plate-sized hole, then dies; the lamp boy will take it dead |
| `rootbeer` root beer | the cooler, scene 1 | any time, one at a time | #8: the guard's price |
| `sunglasses` sunglasses | the suitcase, scene 1 | any time | #10: traded to the goldsmith |
| `shade` windshield shade | the trunk, scene 1 | after #7 | #8: the first reflector, held on the sunny spot |
| `carmirror` door mirror | the wagon's door, scene 1 | after #7 | #9: the second reflector, in the slot at the foot |
| `coppermirror` copper mirror | the goldsmith, scene 4 | #10 | #11: the third reflector, on the top step |

Looked at and never taken: the ketchup packets, six more loud shirts, a folding lawn
chair, jumper cables, and whatever is under the hood.

**Facts the scripts keep** (besides the thirteen the beats set)

| Fact | Means |
| --- | --- |
| `egypt.trunkOpen`, `egypt.coolerOpen`, `egypt.suitcaseOpen` | a lid is open (the painted cut-out shows) |
| `egypt.tookFlashlight`, `egypt.tookRootbeer`, `egypt.tookSunglasses`, `egypt.tookShade`, `egypt.tookMirror` | it has been taken from the wagon |
| `egypt.metCarrier`, `egypt.metScribe`, `egypt.metOverseer`, `egypt.metHaulers`, `egypt.metGuard`, `egypt.metBoy`, `egypt.metGoldsmith` | the first words have been said |
| `egypt.knowsDonkey` | he has been told the donkey's name |
| `egypt.sawSite`, `egypt.sawGallery`, `egypt.sawChamber` | the first arrival has played |
| `egypt.guardAsked`, `egypt.guardDrank` | the guard has been asked to hold the shade; has had his root beer |
| `egypt.beamSeen` | how far Dad has seen the sunbeam get into the gallery (1, 2 or 3) |
| `egypt.boySawSun` | the lamp boy has had his say about the sun indoors |
| `egypt.barkLight`, `egypt.barkAll` | the overseer has called out about that stage of the job |
| `egypt.doorOpen` | the door has opened wide (the chamber draws it open from then on) |
| `egypt.climbed`, `egypt.cameDown` | the stair has been shown whole, going up; coming down (after that it is cut short) |

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| Small sneaker prints going up the track | The opening | Everybody Dad asks; the door; Act Two |
| "the 'wy-fy'" | The water carrier | "He asks that everywhere. It's how he says hello." |
| "I'm not taking my own car apart without a reason." | The trunk and the door mirror, before #7 | #8 and #9 |
| "...the only cold drinks in Egypt." | Looking back down the track | #8, the guard |
| "A little sun in his hand" | #6 | #7; the overseer's "I have only the big one" |
| "Unless you can bend the day around three corners, we are late." | The overseer, after #7 | #8, #9, #11; "Around three corners and in through the door, like it pays rent." |
| "That mirror most of all" | The goldsmith, about his eyes | #10 and #11 |
| A map that "folds eleven ways" | The map | "Unlike the map, it folds the way it came." (the shade) |
| "Dad's taking the next shortcut" | #12 | Not yet. Where it comes out, and when. |
| The boy's own key-ring flashlight | #6 | Left out, by decision. The Rome brief says it is still in Egypt; nothing in this act shows it. |

## Where the scripts differ from the design, and why

1. **The goldsmith trades whenever he is offered the sunglasses**, not only after #7.
   The design's table has the trade needing the rule. But the sunglasses can be had
   from the start, the goldsmith says what is wrong with his eyes as soon as he is
   asked, and Dad is kind: a script that had him refuse to help an old man's eyes
   until it suited him would not be Dad. So he can come away with the mirror early
   ("I don't know what I'll do with a mirror. That has never stopped me taking
   anything."). What waits for the rule is the last step: the top step will not take the
   mirror until he knows what a mirror is for. The beat `egypt.trade` keeps the table's
   `needs` (so the Hint button does not offer it early), and `egypt.topmirror` needs
   `egypt.knowsLight` as well as `egypt.hasCopper`.
2. **The flashlight works without the lamp boy.** The table already says so. What
   is added: when it does, Dad draws the lamp boy's moral himself ("That's what he
   did."), and the script sets `egypt.heardBoy` along with `egypt.knowsLight`, so that
   the Hint button does not send him to hear what he now knows. The lamp boy still
   tells it if asked, and Dad's last line changes.
3. **The beats `egypt.map` and `egypt.reed` change places.** Nothing depends on the
   order, but the Hint button offers the first open beat, and at the very start "I
   should check what's still in the wagon" is the right thing to hear.
4. **The water carrier, not the scribe, saw the wagon fall,** and has the exchange
   about the horses. See the next section.
5. **The stair is climbed by script, never by a click.** The painter measured the
   steps and the landing as ground a figure can stand on, and the scene keeps them
   (Dad stands on them); but a bar across the bottom steps cuts them off from the
   sand, so that no click can walk him up past the guard. The entrance, the stair and
   the guard take him up, along the painter's marks for his feet.
6. **More things to click than the painters' brief names.** Every person; the ways
   between scenes; everything the painters added to a picture and listed in its
   `layout.json`; and `palms` and the gallery's and the chamber's `walls`. The guard
   is two areas (`guard` at the stair, `guard-sun` on the sunny
   spot), the humming wall becomes `door` when it opens, and each piece of luggage is
   two shapes, shut and open, of which one shows. 61 in all.
7. **Small additions with no design behind them:** Dad can hold the shade up
   himself and see that it works (it is how he learns he needs a volunteer); a guard
   given his root beer early owes "one holding"; the dead flashlight can be given to the
   lamp boy; the overseer calls out once when Dad comes back knowing the rule, once
   when his guard takes up the shade and once when the beam is whole.
8. **The door is an oval, and the flashlight's hole is in the air.** The place that
   hums is a door-sized piece of bare wall, 80 pixels wide. A round door big enough
   to walk through would lie over the king's furniture and the sarcophagus, so the
   open door is a tall oval that stands on the floor in that piece of wall. And the
   plate-sized hole opens in the air just past Dad's hand, below his words: on the
   wall behind his head it would be hidden by what he says about it.

## Where a scene's numbers are not the painter's

Everything else is the painter's own number. `briefs/out/check-egypt.mjs` lists these
differences each time it runs, so that none creeps in unnoticed.

| Where | The scene has | Why |
| --- | --- | --- |
| crash: `footprints`, and the arrival | Dad stands at (424, 502), not (458, 484) | a step clear of the steam off the hood |
| crash: `pyramid` | the area takes in the three small pyramids to the right | the name on it is "pyramids" |
| crash: `track` | Dad walks to (500, 372) and the picture changes; he arrives there too | the far end of the track is nine seconds' walk off, and he is a dot there |
| site: the overseer | (470, 520), in front of his stalled sledge; not (360, 430) | at the painter's mark he stood where the shade is held up, and in the beam |
| site: the three haulers | (322, 416), (296, 405), (270, 394): a step down the rope | at the painter's marks the nearest stood under the corner of the awning |
| site: `entrance`, `stair` | Dad stands at (742, 424), beside the guard | he is stopped there, or sent up from there |
| site: `sledge`, `rope`, `scribe-desk` | he stands at (420, 492), (352, 440), (248, 464) | clear of the overseer, of the haulers, and of the awning's own ground |
| site: `water` | only the shoulders of the jars | the corner under them is the way out to the river, and the inventory lies over much of it |
| gallery: `slot-foot` | the area is 13 pixels taller | so that it covers the mirror once the mirror is in it |
| chamber: `hum` | Dad stands at (452, 506), to one side | so that the hole opens beside him and not behind his head |

## What was kept, moved and dropped from the old act

Of the old act's 40 lines (33 `egypt.*`, the two item lines and five hints):

- **31 are kept word for word, with their ids.** Most stay where they were. Moved: the
  two glovebox lines keep their old ids (`egypt.wagon.use`, `egypt.wagon.empty`);
  `egypt.ask.boy` is now asked of everybody; `egypt.ask.door` is asked of the lamp boy;
  the two dinner-plate lines are the flashlight scene; the three door lines are the
  gate; `hint.egypt.mark` is the hint of the beat that is now called `egypt.pass`.
  The lines file marks each of them "kept", and the check holds them to the letter.
- **2 keep their ids with a word or two changed:** `item.reed.look` ("about three
  thousand years ago" is now "about four and a half thousand years ago") and
  `hint.egypt.reed` ("The scribe lost his pen" is now "The scribe's pen has split").
- **7 are dropped:** `egypt.ans.boy`, `egypt.ans.boy2`, `egypt.ans.door`,
  `egypt.need.sheet`, `egypt.got.map` and `egypt.door.steady` belong to the scribe who
  sat by the river and knew about the door. And `egypt.scribe.hello` ("You fell out of
  the sky in a red chariot with no horses"), because Egypt had neither horses nor
  chariots until some nine centuries after Khufu. The man who was there when the wagon
  fell now says it in his own words ("You came down out of the sky in a red box.
  Nothing was pulling it."), Dad's answer is kept exactly ("It has a hundred and forty
  horses. They're resting."), and the reply is the water carrier's: "So is Donkey.
  Nobody calls him a hundred and forty."

`egypt.arrive.3` still says "a thousand years from now". It is four and a half
thousand. It is kept as it was because he does not know that yet: he is "still working
out the tenses".

**When the pictures came, the picture won.** Nine of the new lines were changed to say
what is painted. The haulers stand (they were written sitting): the water carrier's
news, the overseer's first shout ("Why is everybody STANDING?"), Dad's look at them
("Three big fellows and one idle rope.") and their goodbye ("Well. Keep up the good
work." "We are not doing any."). The stair has a rope for a handrail, the doorway is up
a flight of steps and not halfway up the pyramid, and the scaffold is on the face and
not the top. The goldsmith is gilding a small box, not a chair, and his mirror is
propped against a jar. Thirteen lines were added: one for each of the twelve things the
painters put in beyond their brief, and the scribe's line about rushes. The act has 376.

## Historical statements

Every statement about the past that the act makes, who makes it, and how far it has
been checked. The Egyptians are never wrong about their own time; Dad may be, out loud,
and is put right.

What the words mean:

- **On the list**: it is in the design's own list of true things
  (`briefs/LEVEL-egypt.md`), which the act was told to stay inside. Not checked again
  here unless "Read" follows.
- **Read**: found on the page named under the table. The pages were read through a
  tool that fetches a page and reports on it with quotations, so this is one step short
  of reading the page oneself.
- **To check**: not on the list and not read anywhere. Believed, or taken from the
  design's descriptions of the people and the pictures.
- **Dad's guess**: said by Dad, wrong on purpose.

| The statement | Who, and where | Status |
| --- | --- | --- |
| The pyramid is the king's, and its name is "Horizon of Khufu" | Water carrier, `egypt.carrier.horizon.1`; "the Horizon" throughout | On the list. Read (1): "Akhet Khufu", Khufu's Horizon |
| It is being finished now, about 2560 B.C. | The era card; Dad, `egypt.site.pyramid.look2` ("nearly done") | On the list. (1) gives "c. 2600 BC over a period of about 26 years" |
| It is cased in smooth white stone | Dad, `egypt.site.pyramid.look`; "the big white one" | On the list. Read (1) |
| The white stone comes across the river by boat | Dad, `egypt.boat.look`, `egypt.boat.look2` | On the list. Read (1): from the Tura quarries, by boat across the Nile |
| The builders are paid, in bread and beer, every day, and are not slaves | Haulers, `egypt.haulers.free.1`; the day's wages, `egypt.site.desk.look`, `egypt.gallery.dinner.look` | On the list. Read (3): not slaves; bread. Beer: on the list only |
| Gangs have names like "Friends of Khufu" | Haulers, `egypt.haulers.meet.1`, `egypt.haulers.free.1` | On the list. Read (3) |
| Blocks are dragged on sledges; nothing here has wheels | Dad, `egypt.site.sledge.look`; the haulers "pull stone" | On the list |
| Wetting the sand in front of the runners makes the pull far easier: "one man pulls like two" | Hauler, `egypt.haulers.sand.1`; Dad, `egypt.site.sledge.look2` | On the list. Read (2): the right dampness halves the force |
| The tools are copper chisels, wooden mallets, a plumb line; no power, no iron | Dad, `egypt.site.blocks.look` | On the list. Read (1): copper chisels, wooden mallets |
| The gallery's walls step inward, row by row, toward the top | Dad, `egypt.gallery.walls.look` | On the list. Read (1) |
| The chamber is red stone with no pictures and no writing on its walls | Dad, `egypt.chamber.walls.look` | On the list. Read (1): granite; no inscriptions or decoration |
| The sarcophagus is a plain stone box | Dad, `egypt.chamber.sarc.look`, `egypt.chamber.sarc.look2` | On the list. That its lid is off, and leaning on the wall still roped (`egypt.chamber.lid.look`), is the picture's choice |
| There are goldsmiths, gilded furniture and polished copper mirrors | The goldsmith and his bench; `egypt.chamber.treasure.look`; the copper mirror | On the list. The bed with lion's feet and the carrying-chair are from the painters' brief: to check |
| The king is "the king"; nobody says "pharaoh" | Goldsmith, `egypt.goldsmith.king.1`, mishearing Dad's "pharaoh" as "one arrow" | On the list |
| Nobody here knows what a camel is | Water carrier, `egypt.carrier.camels.1` | On the list. Read (4): not a pack animal before the 12th century B.C. |
| No curse is written over the door | Dad, `egypt.chamber.walls.look2` | On the list |
| The building has taken twenty years | Overseer, `egypt.overseer.hum.4` (the design's own line), `egypt.overseer.map`; guard, `egypt.guard.notlong` | **The traditional figure**, and kept as such by decision. It is Herodotus's, written two thousand years later (1); nobody of the time has left a number |
| A scribe keeps the lists, and tallies on bits of pot | The scribe; `egypt.site.desk.look2` | From the design. To check |
| A scribe's pen is properly a rush; a cut reed is a makeshift | Scribe, `egypt.scribe.rush` | Read (5): scribes of this time wrote with a rush chewed to a brush, and the reed pen cut to a split nib came with the Greeks. **Decided:** the reed stays (it is the old act's puzzle), and the scribe says what the proper thing is |
| The inside is lit by oil lamps that a boy keeps filled | The lamp boy, `egypt.lampboy.lamps.1` | From the design. To check |
| Water is carried up from the river on a donkey | The water carrier and Donkey; `egypt.site.water.look` | From the design. To check |
| Mud bricks are shaped in a mold and dried in the sun | Dad, `egypt.site.bricks.look` | From the picture. To check |
| A timber scaffold lashed with rope stands against the pyramid's face, and the stair to the doorway is mud brick with a rope rail | Dad, `egypt.site.scaffold.look`, `egypt.site.stair.look` | From the painters' brief and the picture. To check |
| A guard keeps the stair, and the scribe's list says who goes up | Guard, `egypt.guard.stop` | Invention |
| "There'd be camels" | Dad, `egypt.carrier.ask.camels` | Dad's guess. Put right at once |
| "One day you'll all be free" | Dad, `egypt.haulers.ask.free` | Dad's guess. Put right at once, with some heat |
| "All this for one pharaoh?" | Dad, `egypt.goldsmith.ask.king` | Dad's guess. "The king. Right. One of those." |
| "Walls you could read", and a curse over the door | Dad, `egypt.chamber.walls.look`, `.look2` | Dad's guess. The walls put him right |
| "A hundred and forty horses" | Dad, `egypt.scribe.hello2` | True of the wagon. Nobody here knows the word, and nobody is made to say it |

Not said by anybody any more: that an Egyptian of this time knows a chariot or a horse.
Chariots came to Egypt with the Hyksos, about 1700 B.C. (6).

Pages read:

1. Wikipedia, [Great Pyramid of Giza](https://en.wikipedia.org/wiki/Great_Pyramid_of_Giza): the ancient name; white limestone from Tura for the casing, brought by boat across the Nile; granite from Aswan for the King's Chamber; a granite sarcophagus; interior walls without inscriptions or decoration; the Grand Gallery's walls corbelled inward; copper chisels, wooden mallets, ropes and stone tools; Herodotus's twenty years.
2. University of Amsterdam, Institute of Physics, [news of a 2014 paper](https://iop.uva.nl/content/news/2014/00/prl-egyptian-pyramids.html): the right dampness in the sand halves the pulling force, because the sand does not pile up in front of the sledge.
3. BBC Science Focus, [Were the Egyptian pyramids built by slaves?](https://www.sciencefocus.com/science/were-the-egyptian-pyramids-built-by-slaves): not slaves; bread in great quantity; a crew that painted its name near Khufu's burial chamber, "The Friends of Khufu Gang".
4. Wikipedia, [Camel](https://en.wikipedia.org/wiki/Camel): the dromedary as a pack animal in that part of the world not before the 12th century B.C.
5. University of Michigan Library, [Papyrus: the "paper" of the ancient world](https://apps.lib.umich.edu/files/collections/papyrus/exhibits/diversity/papyrus.html): Egyptians first wrote with a rush chewed to a brush-like tip; pens of reed, cut to a point and split, came after the Greeks.
6. Wikipedia, [Chariotry in ancient Egypt](https://en.wikipedia.org/wiki/Chariotry_in_ancient_Egypt): chariots are thought to have come to Egypt with the Hyksos, about 1700 B.C.

Confirm every one that is not on the list, or change the line, before the game is
called finished.

## How it was checked

Two scripts, both in `briefs/out/`. Neither changes anything in the game.

**`check-egypt.mjs`** (run with node; it needs nothing but the files) does two things.

It **reads** the game's own files against each other: no script names a line that is
not there, no line is left unnamed or is written again in another act's file, every
beat's fact is set by a script and every fact a script reads is set by one, every
carried thing is in `world.js` with its picture on disk, every speaker is in the cast,
no line is over 130 characters, Dad never uses an exclamation mark and nobody of the
time shortens a word, each of the author's 31 lines is still word for word, no number
is marked PLACE, every clickable thing the painters' brief or a `layout.json` names is
there with a look line, every picture a scene shows is on disk, the walk outlines, the
blocked ground, the cut-outs' base lines and the stair's marks are the painter's own,
every way between scenes has a mark to arrive on, and every place Dad is sent to stand
is on walkable ground and can be walked to from every mark he can arrive on (274
routes, found with the engine's own `js/engine/walk.js`). It also shows that no click
can walk him onto the stair.

Then it **plays** them. A small stand-in for the game, with only the calls the scripts
make, runs the scenes' own scripts: the puzzle table row by row, asserting each fact
before and after; the three reflectors in all six orders, with the door staying shut
until the last and each scene showing as much beam as the facts allow when it is built
again; the side roads (flashlight before the lamp boy, the trade before the rule, the
root beer before the shade, the pass shown four ways, the overseer's report at five
stages); and then every clickable thing in every scene Dad can have reached, looked at
twice, used, and offered everything in his pockets, at sixteen moments of the story.
The Hint button is asked at every step of the table, through the engine's own reading
of the game's own story, and each time it gives the hint for the next thing to do. All
376 lines of the act are spoken in the run, each by somebody who is in the scene at the
time.

**`play-egypt.py`** plays the act in the real game, in a headless browser, from the
start-up panel and New game to the Son standing in Rome, and every step is a real
mouse click: a left click on a clickable area to use it, a right click to look, a
click on a thing in the pockets and then on an area to use one on the other, a click
on the sand to walk, a click on a line to say it, a click on Hint. Before it clicks an
area it finds a point where the click really lands on that area, so an area that
something else covers is reported. It goes two ways through. Way A is the puzzle table
in order, looking at everything: shade, door mirror, copper mirror (269 clicks). Way B
is the impatient player: everything out of the car at once, a root beer for the guard
before there is anything to hold, the trade before the rule, the flashlight without
the lamp boy, and then copper mirror, door mirror, shade (80 clicks). It checks the
facts, the pockets and the lines heard after each step, and the light on the stage at
each stage; asks for a hint sixteen times and checks the answer; saves the game
through the menu and loads it again, three times, and sees that nothing has changed
and nobody speaks; and after the act goes back to Dad by his portrait, finds him at
the door, and returns to the Son. It fails on any console error, console warning or
page error, and saves a picture at each moment worth seeing in
`briefs/out/shots-egypt/` (each stretch of the sunbeam as it appears, the hole the
flashlight opens, the door opening, the tunnel, Rome). Both ways take about two and a
half minutes together.

What neither can tell is whether it is funny.

## Not done

- **Two figures.** The guard holding the shade (`guard-shade`) and the goldsmith in
  the sunglasses (`goldsmith-shades`) were being drawn when this was written. The
  scenes ask for them and, while they are not there, keep the plain `guard` and
  `goldsmith`: the guard stands on the sunny spot with his staff, and the painted
  shade hangs in the air beside him. Nothing needs changing in the scenes when the
  figures arrive, but look at the guard's hands against the shade when they do.
- **The long walks.** From the wagon to the track is about seven seconds, across the
  site to the stair seven, and up the gallery seven and a half, at the engine's
  walking pace; the act is crossed three times at least. The scenes do what they can
  (the stair is shown whole once, the far end of the track is not walked to). A
  quicker pace for a figure that is far off, or a second click that skips a walk to a
  way out, would be an engine change.
- **Dad's arm.** While he holds up the shade or the flashlight, the scenes keep his
  arm out by setting the figure's own `act`, which is the engine's business. A call
  for it (`g.hold()`, say) would be cleaner.
