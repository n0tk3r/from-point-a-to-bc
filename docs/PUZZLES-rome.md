# Rome: puzzle document (first draft)

Act Two, the Son's act. Rome, the morning of the Ides of March, 44 B.C. A ten-year-old
has been put out of a temple with the door in time shut inside it. He gets back in, opens
the door exactly as far as a coin, and tosses the coin through.

It is laid out the way the project's puzzle-document method asks, and the way
[PUZZLES-the-present.md](PUZZLES-the-present.md) is: the characters, the puzzle
structure, the location layout, and then the cut-scenes and puzzles in order. Every
puzzle here is written as playable script, in `js/content/scenes/rome-steps.js`,
`rome-street.js` and `rome-temple.js`.

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

Play it: `index.html?scene=rome-steps&lead=son` starts the act. In the full game it
follows Egypt, on a card that reads "Meanwhile, nearly nineteen hundred years later":
Dad's Egypt is about 1920 B.C. by the Bible's count, and 1921 B.C. to 44 B.C. is 1,877
years (`briefs/DATING.md`). The card is the Egypt act's (`egypt-chamber.js`).

How it is tested. `node briefs/out/check-rome.mjs` reads the act as it sits in the
game, walks every route on the engine's own walk map, compares every place with the
painters' measurements, and plays the scripts themselves through three walkthroughs on
a stand-in for the engine (`-v` prints them line by line). `python3
briefs/out/play-rome.py` plays the act in the game itself, in a headless browser, by
real mouse clicks, twice: once by the book (chain A, then B, inside without the coin,
then C), and once the other way round (C, B, A), with the Hint button pressed at every
stage; and then a third, short visit, as a game saved before 7 October would make it.
On the way it goes through every branch of the date seller, and everything else that
was woven in, and checks what is on offer in each list of things to say. It stops on
any console error, and saves a picture of every moment that matters in
`briefs/out/shots-rome/`. Neither is a person playing it. Since round three the check
script also holds each scene's ways out at the edges of the picture (where they lead,
where he walks first, that the ground there can be walked to, that the old ways out are
kept), takes every one of them from every state it explores, and holds the clickable
shapes (no rectangles but the two painted boards; each cut-out and person named for Show);
and the play script leaves each scene by a click in the band along its edge and comes
back, after checking the arrow and the line that says where it goes, and turns Show on
in each scene for a picture, checking that everything is outlined.

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

Puzzles are numbered within this act.

## The idea of the act

Dad, in Egypt, makes tools out of what is in the car. The Son has no car. What he has
is legs, no fear, and a way of making friends in any century. So his act is **errands**:
everyone on the street has a use for a boy who can run, and each errand pays in the
thing he needs. Then comes the one clever thing, which is his own.

| | What he needs | Who has it | What they want first |
| --- | --- | --- | --- |
| **Chain A** | a clean tunic | the washerwoman | the senator's toga run up to the Forum |
| **Chain B** | something for the god | the soothsayer | his breakfast, so that his sacred chickens will feed |
| **Chain C** | light, on a wall in the dark | the fountain, and the sun | nothing: a wish is borrowed |

**The rule of the doors**, the same in every era: a door in time stays where it once
opened, shut and invisible, and it hums. Light thrown on the place opens it, and the
more light, the bigger the door. The Son half knows this, because his key-ring
flashlight did it in the pyramid. Here he has a dead phone, a patch of morning sun on
the wrong part of the floor, and a new silver coin. A little light: a little door.

The player is never stuck on one thing. A, B and C are all open from the first minute,
in any order, and can be mixed. Nothing can be lost, used up wrongly or done too soon.

---

# Act Two: Meanwhile

Rome, the Ides of March, 44 B.C. Morning.

## Characters

- THE SON: ten, lost, delighted; rates Rome out of ten and has an Operation for everything; wants his dad, and a snack, in that order on paper.
- THE DOORKEEPER: keeps the door of the treasury; scores what he sees out of three; wants nothing to change, ever.
- THE SOOTHSAYER: sits on the temple steps with his sacred chickens; has been telling Rome to beware the Ides of March since February; wants his breakfast, and not to climb fourteen steps.
- THE SENATOR: late for the Senate in yesterday's toga; has a magnificent speech about drains; wants his clean toga, and to be looked at.
- THE SNACK-BAR KEEPER: feeds everyone and is owed by everyone; has not drawn breath in eleven years; wants the soothsayer's breakfast taken up the street.
- THE WASHERWOMAN: runs the laundry on "first" and "then"; cleans cloth the Roman way and sees nothing odd in it; wants the senator's toga off her hands.
- THE STREET BOY ("Walnut"): the Son's age, best at nuts on the street; cannot take his eyes off the light-up sneakers; wants a friend, and is the act's hint-giver.
- THE CLERK: counts the Roman People's silver, twice, by lamplight; loses count whenever anyone speaks; wants to reach a number.
- THE DATE SELLER: a Jew from Judea, about fifty, selling dates from Jericho at the kerb; courteous, humorous, unhurried, nobody's fool; keeps the seventh day, prays toward Jerusalem, sends his half-shekel home; wants nothing from the boy, and is waiting for someone. He is part of no puzzle.

## Puzzle structure

```
                         Cut-scene: Not the rest stop
                                      |
        +-----------------------------+----------------------------+
        |                             |                            |
 #1 Take The Toga            #4 Take The Breakfast          #7 Borrow A Wish
   (the street)                 (the street)                  (the street)
        |                             |                            |
 #2 Deliver It               #5 Feed The Soothsayer                |
   (the steps)                  (the steps)                        |
        |                             |                            |
 #3 Collect The Tunic                 |                            |
   (the street)                       |                            |
        |                             |                            |
        +--------------+--------------+                            |
                       |                                           |
            #6 Three Out Of Three                                  |
          (the steps: the doorkeeper)                              |
                       |                                           |
                       +---------------------+---------------------+
                                             |
                                       #8 Tiny Sun
                                       (the temple)
                                             |
                                 #9 Heads, Tails, Edge          the gate
                                       (the temple)
                                             |
                     Cut to: "Meanwhile, about two thousand years later"
```

Goal of the act: **get back to the door, and find out what it does with a coin.** Two
chains of errands meet at the doorkeeper; the third is one borrowed coin that waits
for him inside. Easy on purpose, for a ten-year-old lead: every step is told to him by
someone, in character, before he can be stuck on it. The one step nobody tells him is
the last idea, the coin as a mirror, and he has the pieces of it in his own words.

Story facts, in the order the story file lists them (the Hint button speaks for the
first one that is open): `rome.arrived`, `rome.hasToga`, `rome.delivered`,
`rome.hasTunic`, `rome.hasBreakfast`, `rome.hasIncense`, `rome.inside`, `rome.hasCoin`,
`rome.doorOpen`, `rome.tossed`.

## Location layout

```
+------------------------------------------------------------------------------+
| THE STEPS OF THE TEMPLE (rome-steps)                 he starts here          |
|                                                                              |
|  the Forum beyond          THE DOORS (open)  <- THE DOORKEEPER, in the way   |
|  (statues, a hill)         columns                                           |
|  a handcart, a dog asleep  notice board   fourteen steps                     |
|                            THE SOOTHSAYER and his SACRED CHICKENS            |
|  left edge:      ALTAR   tripod                                              |
|  to the street   THE SENATOR (until his toga comes)   pigeons  carved stone  |
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
until #6, and open to him ever after.

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
Solution:     Talk to her. She looks him over ("A pouch on the belly and a little awning on the
              head. Whoever dresses you enjoys a joke."), asks if he can run, and makes the offer:
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
```

```
Puzzle #2: Deliver It        (Rome · the steps · the senator)        chain A
Needs:        #1
Setup:        A senator stands at the foot of the steps in yesterday's toga, late for the Senate,
              which meets today in the hall beside Pompey's theater. There is an olive stain. He
              will not be seen with it.
Wrong tries:  Show the toga to the doorkeeper  -> "Senators are down there. I am up here. We both prefer it."
              Show it to the soothsayer        -> "Not mine. Mine has known soup. That one has a future."
              Show it to the snack-bar keeper  -> "...in my shop, beside my sauce, out, out..."
              Show it to the street boy        -> "Don't let it touch the ground. Don't let it touch
                                                 ME. I'm mostly ground."
Solution:     Give him the toga: use it with him, or talk to him and say "Delivery!" "A TOGA, boy.
              A bedsheet covers a man asleep. A toga covers a man who matters." "Rome thanks you. I,
              personally, am far too late." He strides off to the Senate and is not seen again.
Gives:        A favor owed. "The laundry lady owes me one tunic."
Teaches:      Handing a thing over: by using it with someone, or by saying so when they talk.
              (Every errand in the act can be finished either way.)
Hints:        Hint button: "I'm carrying a senator's bedsheet. He's the one standing still in a
              hurry, by the temple steps." The street boy: "He's the big angry one at the foot of
              the temple steps. Run."
Plants/pays:  Pays off the washerwoman's errand. His speech is about drains. "It ends when they agree
              with me."
Notes:        He goes because his figure is already wearing a toga and cannot change it on stage:
              the clean one leaves under his arm. Nothing he says looks ahead to the day's events.
              Once the boy has heard of Caesar (the cut-scene in the street), there is one more thing
              to ask him, until he leaves: "Does Caesar have a kid?" See "The family's faith" below.
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
              eleven years. Today his boy has not come and he cannot leave the pot.
Wrong tries:  Pay with the quarter      -> "Who is this? I know every consul's nose. That is not a
                                          consul." "That's George. He's on all the quarters." "...you
                                          pay me later, everyone pays me later."
              Pay with the fountain coin -> "THAT nose I know, that is Caesar, struck this year..."
                                          "I can't spend it, though. It's a borrowed wish."
              Bring the breakfast back   -> "No, no, UP the street, the old one with the chickens..."
Solution:     Talk to him. He feeds the boy before anything else ("you are too thin, everybody is
              too thin, here, eat, eat"), and then: "you have legs, fast legs, take this to the old
              soothsayer on the temple steps." "Tell him he owes me for all eleven, he will say he
              foresaw it, he always foresaw it."
Gives:        The soothsayer's breakfast. And a snack: "Step one: DONE. Nine out of ten."
Teaches:      The same lesson as #1 from the other end: this errand finds him.
Hints:        Hint button: "Something for the god: the chicken man has incense. And no breakfast. The
              snack bar has breakfast." The soothsayer: "My bread and sausage come up from the
              cookshop by the fountain. Not this morning." The street boy says both halves.
Plants/pays:  Pays off "Step one: snacks". Plants no tomatoes: "It only needs ketchup." "What is a
              tomato?" "...No tomatoes. Dad's been saving those little packets for years. He KNEW."
Notes:        "Operation Sausage Express. I won't eat it. I'll just THINK about eating it."
```

```
Puzzle #5: Feed The Soothsayer        (Rome · the steps · the soothsayer)        chain B
Needs:        #4
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
```

```
Puzzle #9: Heads, Tails, Edge        (Rome · the temple · the coin-sized door)        THE GATE
Needs:        #8
Setup:        A door he cannot fit through. "My eye fits. The rest of me has to wait."
Wrong tries:  Go through it        -> "I'm not jumping in there again without a snack. That's a rule I
                                      made up just now and I stand by it." "Also I'm bigger than a
                                      coin. That's the other rule. Physics made that one up."
              Send the quarter     -> "Not the quarter. George is the only other American in Rome. We
                                      stick together."
              Send the phone       -> "It won't fit. Also it's dead. A dead phone is not the message I
                                      want to send Dad."
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

The rules it keeps. Scripture is quoted twice, word for word from the King James
Version, each time by the date seller and each time with its reference said (by the
boy, who learned both by heart): the first clause of Micah 5:2, and Numbers 6:24. Both
end on the King James mark, a comma and a colon, because both verses run on. Everything
else from the Bible is the boy telling it in his own words. Nobody argues, nobody is
laughed at for what he believes, nobody is told what is coming. "Not yet." is said
three times in the act and no more (the check script counts). Nobody says "early":
that word is Little Sister's, in Act Four.

| Where | What happens | The lines |
| --- | --- | --- |
| The street, the first time (a cut-scene, above) | **B.C.** The keeper's cry gives him Caesar; Big Sister's timeline gives him B.C.; "before Christ" does the rest. Operation Don't Wreck Anything. | `rome.street.cry`, `rome.street.bc.1` to `.4` |
| The fountain, on taking the coin (#7) | **The coin.** The tribute money (Matthew 22:17-21), in his own words, with the point of it right. "This isn't that Caesar. Not yet." | `rome.fountain.caesar.1` to `.4` |
| The senator, asked "Does Caesar have a kid? A kid like that could get in ANYWHERE." (on offer once he has been to the street, until the senator leaves) | **Caesar's great-nephew.** "Caesar has no son. There is a great-nephew: Gaius Octavius, eighteen, off at his books in Apollonia." "Nobody gives the boy a thought. I mention him only because I am thorough." "I know another Caesar! Caesar AUGUSTUS. Luke 2:1. He counts everybody. It's how the Christmas story starts." "Augustus. There is no such name. I know every name in Rome that matters." "...Not yet." | `rome.senator.ask.caesar`, `rome.senator.ans.caesar.1` to `.5` |
| The clerk, asked "What's on all the wax pads?" | **Herod.** "Accounts. Judea's: Antipater's, and his son Herod's, from Galilee, where the young man governs." "Herod? KING Herod? The bad king in the Christmas story?" "Herod is no king. He is a procurator's son with expensive tastes. I have the figures." "...I'd count him twice. I'm just saying." (No tag here: three is the limit.) | `rome.clerk.ask.judea`, `rome.clerk.ans.judea.1` to `.4` |
| The stepping stones, looked at a second time | **The road.** "Paul walks into Rome on a road like this. The Appian Way: it's on my Bible map. The church comes out to meet him. Not yet." (Acts 28:15 names two stations on that road and not the road, so he has the name from a map.) | `rome.stones.look2` |
| The date seller | below | `rome.dateseller.*` (34 lines) |

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
have looked." "Jericho? The Jericho with the WALLS?" "You know of the walls. In that
hat. ...The same Jericho. The palms have done better than the walls." That the boy
knows Jericho is why the man talks to him at all.

| He asks | What is said | Notes |
| --- | --- | --- |
| "Can I try one? I'm between snacks." | "For a boy who knows of Jericho, the first is a gift. Here." He holds one out on his open hand; the boy takes it. "It's candy. It's candy that GROWS. Nine out of... OW. There's a rock in it!" "The stone. That part is a palm tree that has not begun. I ought to charge you for the tree." "Nine out of ten. One off for the surprise rock." | Once: one gift. It is eaten; nothing is carried away. |
| "Everybody here has a statue to pray to. Which one's yours?" | "None. We have one God: the God of Abraham, of Isaac and of Jacob. He made heaven and earth." "Abraham, Isaac and Jacob? I KNOW them! That's who we pray to at my house!" "At your house. ...Then the world is larger than Rome has told me." "Rome finds us Jews very funny: a great Temple in Jerusalem, and no statue in it." "Pompey himself went in, nineteen years ago. He found no image. Not one." "I ask them how they would carve the One who made the stone. They buy their dates and go." | The joke is his, told on himself. He says nothing about anybody else's gods. |
| "What do you pray for?" (on offer once the one above has been asked) | "For the one who is promised. Every day, facing Jerusalem. The prophet Micah has told us his town:" "'But thou, Bethlehem Ephratah, though thou be little among the thousands of Judah,'" The boy turns away, to us: "Micah 5:2! That was my line in the Christmas program. ...Bethlehem. I know SO much about Bethlehem." "I've never wanted to tell anybody anything so much. It's not mine to tell. That news has its own angels." And back to the man: "Mister? It's going to be worth the wait. If I were you, I'd keep watching that town." A moment. "...That was not a guess. I will not ask you what it was. But I will watch." "And for you, young sir: 'The LORD bless thee, and keep thee:'" The boy's head goes down as it does every Sunday, hands folded, before he knows it has. "Numbers 6:24! Pastor says that at the end of church. The very same words. ...Thanks, mister." | The heart of the act. Once: a blessing is not given twice for the asking. |
| "Bye, mister." | "Go well, young sir. Come any day but the seventh. That day I rest, and Rome always wants dates." | No weekday is named anywhere: the game does not say what day of the week the Ides fell on. |

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
| Senator | steps, until #2 | his clean toga | his thanks, which the washerwoman honors | why he is late; the stain; Caesar's great-nephew; Dad |
| Snack-bar keeper | street, behind his counter | a boy with legs | the breakfast, and a snack | the quarter; pizza; who owes him; Dad |
| Washerwoman | street, by her basket | the toga taken up the hill | the toga, then the tunic | how cloth is cleaned; the tunic; Dad |
| Street boy | street, on the curb | to see the shoes light up again | hints, and a friend | the walnut game; the temple; what to do next |
| Clerk | temple, at his table | to reach a number | nothing | what he counts; the statue's feet; the hum; the accounts from Judea; Dad |
| Date seller | street, at the kerb by the last stepping stone | nothing | one date, eaten on the spot; a blessing | the dates; his God; what he prays for; (shown the breakfast) the soothsayer's hens |

**Things that are carried**

| Thing | Comes from | Used for | Leaves him |
| --- | --- | --- | --- |
| Senator's toga | the washerwoman (#1) | given to the senator (#2) | at #2 |
| Small tunic | the washerwoman (#3) | one of the doorkeeper's three (#6) | never: "Bring it back clean." |
| Soothsayer's breakfast | the snack-bar keeper (#4) | given to the soothsayer (#5) | at #5 |
| Incense box | the soothsayer (#5) | one of the doorkeeper's three (#6) | if he sets it down at the god's feet |
| Silver coin | the fountain (#7) | his mirror (#8); then tossed (#9) | at #9, to Nevada |
| Dead phone | his pocket | nothing. Tried on the hum, the sun, the door, and five people | never |
| Quarter | his pocket | nothing. The keeper cannot place the nose | never |
| Pack of gum | his pocket | nothing. The street boy likes it: "It's fighting back." | never |

**Story facts the scripts keep**, besides the ten that are beats: `rome.knowsRule` (the
doorkeeper has said what he lets in), `rome.metSoothsayer`, `rome.metSenator`,
`rome.metUrchin`, `rome.metClerk` (first words said), `rome.sawStreet`, `rome.sawInside`
(arrival remarks made), `rome.knowsWash` (he has heard how cloth is cleaned),
`rome.offered` (the incense is at the god's feet), `rome.knowsBC` (he has heard the
keeper's cry and worked out when he is: it puts the question about Caesar on offer),
`rome.metDateSeller`. What the date seller has already given (the date, the blessing),
and what the boy has noticed at the cage, are kept by the lines themselves having been
said, as the engine counts them.

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
| B.C. is "before Christ" | The street | Act Four, at the gate: what makes "Daddy's EARLY!" land |
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
| A door the size of a coin, left open | #8 | Not yet. He is still in the temple, and now has no coin. |
| A boy who would like to see the shoes light up again | The street | Not yet. Walnut is owed two nuts. |

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
| The Bible has a Caesar Augustus, who has everybody counted, and the Christmas story begins with him | The Son, `rome.senator.ans.caesar.3`, in his own words, with the reference | **Checked.** Luke 2:1, facts-home (`kjv.luke2.1`): "a decree from Caesar Augustus, that all the world should be taxed" ("taxed" is the King James word for enrolled). |
| There is no such name as Augustus, this morning | The senator, `rome.senator.ans.caesar.4` | **Checked.** facts-home (`rome.octavius`): the Senate gave him the name in 27 B.C. (Suetonius, Augustus 7.2). |
| Antipater has charge of Judea, and his son Herod, a young man, governs Galilee | The clerk, `rome.clerk.ans.judea.1` | **Checked.** facts-home (`rome.herod.galilee`): Josephus, Antiquities 14.143 and 14.158. No age is given for Herod, as the checker asks. |
| Antipater is a procurator | The clerk, `rome.clerk.ans.judea.3` | **Checked.** The same: "so he made him procurator of Judea" (Whiston's Josephus). |
| Their accounts are on a clerk's table in the treasury at Rome | The clerk, `rome.clerk.ans.judea.1` | **To check.** The brief's invention. (Pompey made Judea pay tribute to Rome, as this writer remembers Josephus; that was not read today, and where such accounts were kept is not known to him.) |
| Herod has expensive tastes | The clerk, `rome.clerk.ans.judea.3` | The clerk's opinion, and the brief's line. Not sourced for 44 B.C. |
| Herod is not a king | The clerk, `rome.clerk.ans.judea.3` | **Checked.** facts-home (`rome.herod.galilee`): named king by the Senate in 40 B.C. |
| A King Herod is the bad king of the Christmas story | The Son, `rome.clerk.ans.judea.2` | **Checked.** Matthew 2:1, facts-home (`kjv.matt2.1`): "in the days of Herod the king"; that it is the same Herod, facts-home (`rome.herod.galilee`). |
| Paul came into Rome by road, and the brethren came out along it to meet him | The Son, `rome.stones.look2`, in his own words | **Checked.** Acts 28:15-16, facts-home (`kjv.acts28.15-16`). |
| The road was the Appian Way | The Son, `rome.stones.look2` | **Checked.** facts-home (`rome.appian`): Acts names two stations on it (Appii forum, The three taverns) and not the road. So the boy has the name from the map in his Bible, and says so. |
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
| **QUOTED:** "But thou, Bethlehem Ephratah, though thou be little among the thousands of Judah," | The date seller, `rome.dateseller.ans.pray.2`; the reference by the Son, `.ans.pray.3` | **Checked**, exact: Micah 5:2, the first clause, facts-home (`kjv.mic5.2`). The verse runs on, so the quotation ends on its comma. |
| Angels bring the news of that birth | The Son, `rome.dateseller.ans.pray.4` | **Checked**, read 2026-10-07: Luke 2:9-13, Bible Hub, King James Version. An allusion, in his own words; not on the checker's list of verses. |
| **QUOTED:** "The LORD bless thee, and keep thee:" | The date seller, `rome.dateseller.bless.1`; the reference by the Son, `.bless.2` | **Checked**, exact: Numbers 6:24, facts-home (`kjv.num6.24-26`). The verse ends with a colon, and so does the quotation. |
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

**What the Son gets wrong out loud, on purpose.** Togas are bedsheets. The sacred
chickens are pets. The temple is a church and a bank. The jars in the counter hold
soup. The walnut game is marbles. MARCVS is misspelled, and VOTA might mean vote. The god
has a blanket on his head and a hook knife. Dates are giant raisins, and the stone in
one is a rock. No Roman agrees with any of it. About the Bible he is not wrong: what he
tells, he tells in a ten-year-old's words, and he gets it right.

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

**One fact outside this act that these sources bear on.** Big Sister says in Act Four
(`nevada.coin.read.2`, marked "To check" in CHARACTERS.md) that Caesar "was the first
living Roman to put his own face on Rome's coins". The Roman currency page says the
opposite: "living Romans had appeared on coinage before", and that Caesar's portrait
"marked the third instance in Roman history where a living individual was depicted".
(Her line is being reworded by whoever writes Act Four.)

---

## What comes next (not written)

- The Son is still in the temple. The door is open, the size of a coin, and he has
  nothing left to send through it. Something could come back the other way.
- The tunic has to go back clean, and Walnut is owed two nuts.
- Whether Dad's door in Egypt, opened as wide as a whole sun, comes out here.
