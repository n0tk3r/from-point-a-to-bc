# Rome: puzzle document (first draft)

Act Two, the Son's act. Rome, the morning of the Ides of March, 44 B.C. A ten-year-old
has been put out of a temple with the door in time shut inside it. He gets back in, opens
the door exactly as far as a coin, and tosses the coin through.

It is laid out the way the project's puzzle-document method asks, and the way
[PUZZLES-the-present.md](PUZZLES-the-present.md) is: the characters, the puzzle
structure, the location layout, and then the cut-scenes and puzzles in order. Every
puzzle here is written as playable script, in `js/content/scenes/rome-steps.js`,
`rome-street.js` and `rome-temple.js`.

**Status: first draft.** The three places, the seven people, the five things, the ten
beats and the rule of the doors are the design (`briefs/LEVEL-rome.md`). What is
invention here, to keep, change or throw out: every line that is not an old one
(seventeen are kept word for word: the eleven the design names, his two old hints, and
the four looks at the coin); why each person wants what they want (the keeper's absent
boy, the senator's olive stain, the chickens that will not feed); the doorkeeper scoring
people out of three; the keeper feeding him on sight, which is "Step one: snacks" paid
off; the street boy's name, Walnut; the incense set down at the god's feet; the dog
asleep on the Forum, which he wants; and the three things in his pockets doing small
duty as wrong answers.

Play it: `index.html?scene=rome-steps&lead=son` starts the act. In the full game it
follows Egypt, on a card that reads "Meanwhile, about twenty-five hundred years later".

How it is tested. `node briefs/out/check-rome.mjs` reads the act as it sits in the
game, walks every route on the engine's own walk map, compares every place with the
painters' measurements, and plays the scripts themselves through three walkthroughs on
a stand-in for the engine (`-v` prints them line by line). `python3
briefs/out/play-rome.py` plays the act in the game itself, in a headless browser, by
real mouse clicks, twice: once by the book (chain A, then B, inside without the coin,
then C), and once the other way round (C, B, A), with the Hint button pressed at every
stage. It stops on any console error, and saves a picture of every moment that matters
in `briefs/out/shots-rome/`. Neither is a person playing it.

Where things are: every place in the three scene files is the painter's own
measurement of the finished picture (`layout.json` beside each picture in
`art/scenes/`), or was set by eye against the picture with the people standing in it
(their clickable shapes, the things the painters added after their lists were made).
A few places differ from the painters' on purpose, and the check script lists each with
its reason: places to stand that the engine will not let anyone stand on; places that
lie under the inventory bar, which covers the bottom of the picture whenever the game
is waiting for a click; and the soothsayer's corner of the steps, which is wired for
the picture without the folding stool and the second staff that were first painted
there.

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
        |  up the street / down the street                 | through the doors
+-----------------------------------------------+  +---------------------------+
| THE STREET (rome-street)                      |  | INSIDE THE TEMPLE         |
|                                               |  | (rome-temple)             |
|  far end: the Forum, small and sunlit         |  |                           |
|  WASHING LINES overhead, a SMALL TUNIC on     |  |  THE STATUE, feet tied    |
|  the low one    apartments, a songbird, a cat |  |  offering bowl            |
|  SNACK BAR, sign, price list  writing  shrine |  |  THE PLACE THAT HUMS      |
|  THE KEEPER            on the walls FOUNTAIN  |  |  (left wall, in shadow)   |
|  laundry basket                               |  |  chests, a cat      rack  |
|  THE WASHERWOMAN   stepping stones            |  |  THE CLERK at his table   |
|                    THE STREET BOY             |  |  SUNLIGHT ON THE FLOOR    |
|                           jars, a cart wheel  |  |  out: the door leaves     |
+-----------------------------------------------+  +---------------------------+
```

Three scenes. The street and the steps are open from the start; the temple is shut
until #6, and open to him ever after.

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
The way to the street, which is behind the laurel and easy to miss.
*Also:* the three things in his pockets arrive with him, without fuss: a dead phone, a
quarter, half a pack of gum. He plays the act alone: Dad is still in Egypt, standing at
his door, and there is nobody to switch to.

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
              the backpack. I'm a lumpy Roman." "...Three out of three." "YES." "The cap." "The cap is
              load-bearing." "...Go in. Walk. Touch nothing. The clerk is counting."
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
Gives:        The silver coin.
Teaches:      Nothing yet, and that is the point: it is a shiny thing picked up because it was there.
              What it is for comes later (#8).
Hints:        Hint button (only once he is inside without it): "That fountain is full of other
              people's wishes. I only need to borrow one." The street boy, asked how to put light on
              a wall: "Shiniest things on this street are the new silver ones in the fountain. They
              flash like fish."
Plants/pays:  Plants shiny, twice. The keeper names the face on it (Caesar, "struck this year"): the
              Son never learns why that matters. Big Sister does, in Act Four.
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
washing lines, the laundry basket, the stepping stones, a cat ("Cats were already like
this") and the songbird it is watching ("The cat over there is a big fan. A BIG fan."),
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

## Ledger for this act

**People**

| Who | Where | Wants | Gives | Talks about |
| --- | --- | --- | --- | --- |
| Doorkeeper | steps, in the doors | a boy, a clean tunic, something for the god | the way in | the three things; what is inside; Dad |
| Soothsayer | steps, sitting | his breakfast, for him and for the birds | the incense box | the chickens; the temple; the boy's future |
| Senator | steps, until #2 | his clean toga | his thanks, which the washerwoman honors | why he is late; the stain; Dad |
| Snack-bar keeper | street, behind his counter | a boy with legs | the breakfast, and a snack | the quarter; pizza; who owes him; Dad |
| Washerwoman | street, by her basket | the toga taken up the hill | the toga, then the tunic | how cloth is cleaned; the tunic; Dad |
| Street boy | street, on the curb | to see the shoes light up again | hints, and a friend | the walnut game; the temple; what to do next |
| Clerk | temple, at his table | to reach a number | nothing | what he counts; the statue's feet; the hum; Dad |

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
`rome.offered` (the incense is at the god's feet).

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
| Caesar's face on a new coin | The keeper, shown the coin | Act Four, #6: Big Sister reads it |
| "Why is the sky DOWN?" | #8 | Act Four, #5: it fell out of the sky and hit his hat |
| "... It didn't come back down." | #9 (the old line) | Act Four, #5 |
| Dad's ketchup packets (his running gag) | CHARACTERS.md | #4: "He KNEW." |
| A dog, which he asks for every birthday | The dog asleep on the Forum: "Dad says we'll see. We never see." | #9 (the old line): "Edge, we get a dog." |
| "Dad says EVERYTHING is the wind." | The old line, at the hum | The clerk, about the noise by that wall at dawn: "That was... probably the wind." "That is what I decided." |
| "Bring it back clean." | #3 | Not yet. He still has the tunic. |
| A door the size of a coin, left open | #8 | Not yet. He is still in the temple, and now has no coin. |
| A boy who would like to see the shoes light up again | The street | Not yet. Walnut is owed two nuts. |

---

## History: every statement made in the act

The rule is the one in [CHARACTERS.md](CHARACTERS.md): people of the time are never
wrong about their own time, and nothing goes down as **Checked** from memory. Each row
was read in the source named, on 2026-10-06. **To check** means believed right and not
confirmed. `briefs/LEVEL-rome.md` lists most of these as true; the last column says
whether this draft found them in a source.

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

Sources: Wikipedia, [Assassination of Julius Caesar](https://en.wikipedia.org/wiki/Assassination_of_Julius_Caesar),
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
has a blanket on his head and a hook knife. No Roman agrees with any of it.

**What nobody says.** Nobody on screen knows what will happen to Caesar today, and the
game neither shows it nor says it. The soothsayer does not know why the day is bad. The
senator hurries off to an ordinary meeting. The keeper knows Caesar as a nose on a coin.

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
