# The present: puzzle document

The part of the game that starts in the present, with the rest of the family: Mom,
Big Sister (13) and Little Sister (7). At home, that evening, they pray, go through the
house, and find out where Dad's phone was last seen and what he last said. Then they
drive to the middle of the Nevada desert, find a witness, learn that the government
has been closing parts of the desert for "elevated radiation", and open a door in
time exactly the size of a coin. Through it they talk to the Son; with a sun shade
from Grandma Jolene's store they make it as wide as a windshield, and walk through.
Then the men in gray take Grandpa Joe away in a limousine, and the opening of Act
Five is played as Grandpa Joe and his raccoon, Ranger.

It is laid out the way the project's puzzle-document method asks: for each act the
characters, the puzzle structure, the location layout, and then the cut-scenes and
puzzles in order. Every puzzle here is playable now.

**Status.** Act Three was remade on 2026-10-07 on the author's instructions, in two
passes. In the morning: a house with an upstairs instead of one room; ten puzzles
instead of three; Mom as clever as her elder daughter, with a territory of her own
(music, the stage, her books, the Founders and the United States); and the family's
Christian faith as part of how they live and talk. In the evening, when the rooms had
been painted: each sister has a room of her own (Little Sister's is a kingdom of
chickens; Big Sister's is the attic, the Retreat); the house is five rooms; there is an
eleventh puzzle (the flashlight is dead, and the only batteries are in Big Sister's
sound machine); every date before Christ is the Bible's count, as Archbishop Ussher
counted it, and Big Sister's timeline says so (see "How the game counts the years" in
[CHARACTERS.md](CHARACTERS.md)); and chickens run through the whole game, beginning
here. The outline (phone location, Nevada, witness, closed government areas), the three
characters' abilities and Little Sister's line "Daddy's not lost. Daddy's EARLY." are
the author's. The rest is invention to make that outline playable: keep, change or
throw out. Four of the five rooms are fitted to their finished paintings by the
painters' own measurements. The fifth, the landing, is fitted to its painting as it
stands, and waits for one repaint (the attic ladder let down, and Little Sister's door
as hers alone): until then the ladder is clicked at the hatch and its cord. Act Four
was put onto its painting on the same day; its part of this document is its own
writer's, and has been brought into step with the new years (the notice now seals
sectors 44 and 1921) and the chickens. On 10-12 October (round twelve) Act Four was
expanded and Act Five begun, on the author's instructions of 9 and 10 October; all of
it is built, and its part of this document was brought up to the game as built on 12
October.

<!-- MAP-15D -->
**Round fifteen** (14 October; `briefs/MAP-15.md`): the game has a map screen (DESIGN.md,
section 8, "The map, and the Timer"). Act Three's map is Dad's pencil floor plan of the house,
and Act Four's and Act Five's is Grandpa Joe's road map of Nevada: each act's "Location layout"
has a note on its own. The one change in the acts' files is the store's: what its front door
did as the three went out (they are not inside any more, `nevada.inStore`) is done by the
scene's `leaving` now, so that going out by the map does it too. No puzzle, beat or line
changed. The plays of the house, the store and the limousine were run again on the engine with
the map, each without a problem (the house in 814 clicks; all 246 of the store's lines, going
out and in again five times; all 148 of the cut-scene's and Act Five's), and the acts' checks
say exactly what they said before.

<!-- DRIVE-16M -->
**Round sixteen** (16 October; `briefs/DRIVE-16.md`): the limousine's windows. The author found
them "weird, the outside needs to go past not look like mirrors": the desert outside is now the
world itself going by in perspective, each side its own country (Act Five's "Location layout" has
a note). The one change in the act's files is the limousine scene's two moving things in its
windows; no puzzle, beat or line changed. The limousine's play and the act's integration play were
run again on it, each without a problem (all 148 of the cut-scene's and Act Five's lines), and the
act's check, which looks at the two drives now where it looked at the two strips, is clean.

Play it: `index.html?scene=home-living-room` starts Act Three and
`index.html?scene=nevada-roadside` starts Act Four. In the full game it follows Rome,
on a card that reads "Meanwhile, about two thousand years later". The other four rooms
of the house open the same way, with the facts that get you there:
`?scene=home-landing&lead=bigsis&flags=home.arrived`,
`?scene=home-study&lead=mom&flags=home.arrived,home.keyInPiano,home.hasKey,home.studyOpen`,
`?scene=home-lilsis-room&lead=lilsis&flags=home.arrived`,
`?scene=home-bigsis-room&lead=bigsis&flags=home.arrived,home.flashTaken`.
Act Four's store opens with `?scene=nevada-store&lead=mom&flags=nevada.arrived`, and
Act Five with `?scene=nevada-limo&lead=grandpajoe` (its opening plays first).

Puzzles are numbered within each act for now: Act Three's are #1 to #11. Act Four's
still carry the numbers they had when Act Three had four puzzles (#5 to #9), and want
renumbering when that act's revision is merged. <!-- NEVADA-12W --> Round twelve (10-12
October) expanded Act Four with Grandpa Joe, Grandma Jolene, Ranger and the store: its new
puzzles are #10 to #13, the act's gate is now #13 (the family walks through the door), and
"Act Five opens" (#14, #15, in a limousine) follows it, before the ledger. Where the ledger
names a puzzle, it says which act. When the whole game has a puzzle document they take
their place in one run of numbers.

## The idea of the chapter

Dad and the Son solve puzzles across time. Mom and the girls solve them **across each
other**: three people in one place, and every puzzle needs the right one.

| | What only she can do | In Act Three | In Act Four |
| --- | --- | --- | --- |
| **Mom** | Adults listen to her, and she knows her husband, her piano and her country | Sees the key in her piano; answers the question about the wedding; winds the tape; knows the year the vault wants | Gets the witness to talk; knows the car; buys the mirror shades; asks Grandpa Joe to play, and to hold the light |
| **Big Sister** | Remembers the fact | Reads the riddle (eighty-eight keys); hears which note the key is under; knows the year behind the password; and it is her sound machine, so only she may take its batteries | Knows the coin, and reads the notice for what it means; trades with Ranger; works out the rule of the doors |
| **Little Sister** | Fits in small places and can distract anybody | Gets under the keyboard and into the closet under the stairs; owns the flashlight, and the fort it lives in; knows her brother's password, and chickens | Asks the man in gray two hundred questions; is the one the hens will listen to |

The player switches between them with the portraits at the top left. In the house they
go about TOGETHER: when the one being played takes the stairs or a door, the other two
come too. Trying a job as the wrong person is never a dead end: she says, in her own
way, why it is not hers, and that is the hint. The Hint button does the same: the one
whose job it is says what to try, and the other two say whose job it is. A carried
thing can be handed to either of the others (hold it, click her or her portrait).

---

# Act Three: Five Places Set

Home, the present, 9:40 in the evening.

## Characters

- MOM: classy, refined and loving, and as clever as her elder daughter; plays the piano, thinks like a stage manager when things go wrong ("Places, girls."), reads lives of the Founders the way other people read thrillers; prays before she does anything else; wants all five of them at one table.
- BIG SISTER: thirteen, has read every book in the house; knows the year of everything; says "Fun fact:" where her mother says "A matter of record:"; wants to be the one who works it out. Has made the attic into a spa retreat, and tonight is the one thing in it that is not calm.
- LITTLE SISTER: seven, small but mighty; fearless (BRAVE-scared at the very most), bossy, loving, and certain about everything, chickens most of all; has started before you have finished explaining; gives orders to the flock, to her sister and, when she can get away with it, to her mother; adds her own postscript to a prayer; wants to help, right now. Her favorite, General Feathers, went on the trip in Daddy's suitcase, to keep an eye on him.
- DAD (a voice on the voicemail, and on his own answering machine): is either driving or lost, and is never lost. Signs his notices "THE MANAGEMENT".
- THE SON (a voice on the toy alarm on his bedroom door): "Operation No Girls." His door says NO GIRLS ALLOWED, and a toy blaster hidden over it backs that up. He still wants a dog.

The family are Reformed Christians, and it shows the way music shows in this house:
grace is said, the Bible by Dad's plate is read after supper, the children know their
verses, and when Dad does not come home the first thing Mom does is pray. How that is
written (King James only, exact and brief, inside quotation marks; the reference said
aloud only where it is natural, which in this act means by Big Sister, and every one
listed; hymns named, never quoted; nobody preaches) is in [CHARACTERS.md](CHARACTERS.md).
<!-- PASS-17H: the author's rule of 16 October (round seventeen) -->

## Puzzle structure

```
                  Cut-scene: Voicemail, for the ninth time (and a prayer)
                                      |
            +-------------------------+----------------------------+
            |                                                      |
   #1 The Other Eighty-Eight                           #4 The Retreat Goes Dark
      (Big Sister or Mom reads Dad's riddle;              (the closet is too dark; Little Sister's
       or either of them plays, and hears                  own flashlight, from her fort, is dead;
       one dead note)                                      Big Sister gives up the batteries out of
            |                                              her sound machine, up in the attic)
   #2 The Key In The Piano                                         |
      (Mom sees it, Big Sister hears it,               #5 Plug In The Router
       Little Sister gets it)                             (Little Sister, in the closet under the
            |                                              stairs, by flashlight)
   #3 Open Trip Headquarters (whoever holds the key)               |
            |                                                      |
     +------+------------------+----------------------+            |
     |                         |                      |            |
 #6 Read Dad's Note      #8 Wind The Tape       #10 We The People  |
    (Big Sister: 1928)      (Mom, with Dad's        (Mom: 1787)    |
     |                       pencil)                -> the spare   |
     |                         |                       car key     |
     +------------+       #9 Play The Message          |           |
                  |          (any of them)             |           |
                  +------------------------------------|-----------+
                  |                                    |
          #7 Answer The Question (Mom)                 |
             -> the map: one dot                       |
                  |                                    |
                  +------------------+-----------------+
                                     |
                      #11 Leave For Nevada      THE GATE
                      (needs the dot, the message and the car key)
```

Goal of the act: **find where the phone was last seen, hear what he last said, and get
a car key.** Chain A (#1 to #3) opens the study. Chain B (#4, #5) is open from the first
line, takes them into both sisters' rooms, and feeds chain C. Behind the study door three
chains can be done in any order: C (#6, #7: the computer), D (#8, #9: the answering
machine) and E (#10: the vault). Easy on purpose: these are the first puzzles for a team
of three, and each teaches one rule of playing them. #2 teaches that each of them can do
something the others cannot. #3, #4 and #6 teach that they can hand things to each
other. #4 teaches that the house is more than one room, and that a thing may be
somebody's to give and nobody else's to take.

The beats, as the game has them (`js/content/acts/home.js`), twelve of them:
`home.arrive`, `home.riddle` (#1), `home.key` (#2), `home.study` (#3), `home.batteries`
(#4), `home.router` (#5), `home.note` (#6), `home.login` (#7), `home.tape` (#8),
`home.message` (#9), `home.vault` (#10), `home.leave` (#11).

## Location layout

```
 THE ATTIC
+----------------------------------------------------------------------------------+
| THE RETREAT (home-bigsis-room): Big Sister's            two skylights, the moon  |
|                                                                                  |
|  round    plants      BOOKCASE (by color)   THE SOUND TABLE:     her DESK   her  |
|  window   salt lamp   + her TIMELINE        the SOUND MACHINE    (the novel BED  |
|           robe and      on the wall         (the only batteries) on cards)       |
|           towels        over it             + the fountain                       |
|                                                                                  |
|  THE HATCH (the way down)    her RULES, on an easel     exercise mat             |
+-----|----------------------------------------------------------------------------+
      |  the attic ladder
 UPSTAIRS
+-----|----------------------------------------------------------------------------+
| THE LANDING (home-landing)                                                       |
|                                                                                  |
|  top of the  THE SON'S DOOR  hamper  LITTLE SISTER'S  THE ATTIC  hall     DAD'S  |
|  stairs      (NO GIRLS       photos  DOOR (BEWARE     LADDER     table    STUDY  |
|  window      ALLOWED: toy            OF CHICKENS)     (THE       (key     DOOR + |
|     |        alarm, booby               |             RETREAT)   bowl)    HIS    |
|     |        trap; shut all act)        |                        the trip NOTICE |
|     |        his school bag             |                        countdown  |    |
|     |        - - - - - - - the railing: the living room below - - - - -    |    |
+-----|-----------------------------------|-----------------------------------|----+
      |                                   |                                   |
      |    +------------------------------+---------+   +---------------------+------------+
      |    | LITTLE SISTER'S ROOM (home-lilsis-room)|   | DAD'S STUDY (home-study)         |
      |    |  her drawings  window  MY CHICKENS     |   |  corkboard  window  WALL MAP     |
      |    |  THE FLOCK     (paper  (the chart)     |   |  DESK + COMPUTER    biplane      |
      |    |                rooster)   rooster lamp |   |  + Dad's note       globe        |
      |    |  BLANKET FORT   tea party   her BED    |   |  ANSWERING          shelves +    |
      |    |  + her flashlight          + the PILLOW|   |  MACHINE            FAMILY VAULT |
      |    |  (NO BIG SISTERS)          (RESERVED)  |   |  banner: TRIP HEADQUARTERS       |
      |    |  HEN HOUSE         THE NEST     door   |   |  door    things that did not fit |
      |    +----------------------------------------+   +----------------------------------+
 DOWNSTAIRS
+-----|----------------------------------------------------------------------------+
| THE LIVING ROOM (home-living-room)        (the landing and its three doors above)|
|   stairs                                                                         |
|   window    MOM'S      kitchen   WE THE    clock    PIANO     FRONT DOOR         |
|   photos    BOOKCASE   (look)    PEOPLE             (the key   (the gate)        |
|   CLOSET UNDER                   (framed)            is in it)  sampler over it  |
|   THE STAIRS (the router)                                       coat hooks       |
|                                                                                  |
|   DAD'S ARMCHAIR (its back to us)                 DINNER TABLE, set for five,    |
|   + his CROSSWORD + his PENCIL                    running away from us           |
|                                                   + the family BIBLE at its head |
|   Here: Mom, Big Sister, Little Sister                                           |
+----------------------------------------------------------------------------------+
```

Five scenes, one painting each, each seen through one camera. Ways between them:
living room `stairs` <-> landing `stairs`; landing `lilsis` <-> Little Sister's room
`door`; landing `ladder` <-> the Retreat's `hatch`; landing `study` <-> study `door`
(once unlocked). Each way can also be taken across the edge of the picture, by a click
in the band along that edge, where the pointer becomes an arrow and the label says where
it goes (`edges` in each scene): the living room's left and top edges go up the stairs
(the landing is the top of that picture); the landing's left and bottom edges go down
them, its top edge up the ladder to the Retreat, and its right edge into the study once
the study is open; the study's left and bottom edges, Little Sister's right and bottom
edges and the Retreat's bottom edge go out to the landing. The landing seen from below,
in the living room, is a way up too. The front door of the living room is a door in a
wall, not an edge: it is the only way out of the house, and it leads to Act Four. The Retreat has its own music (one slow tune in D major, from
the sound machine) until its batteries are taken: after that the house's tune is heard
up there too.

<!-- MAP-15D -->
**The map (round fifteen).** The Map button (or M) shows the house as Dad's pencil floor plan
on squared paper: the ground floor on the left, upstairs on the right with the attic above it,
each room that is a place drawn in plan with its things, and Dad's arrow "up" from the foot of
the stairs to the landing (DESIGN.md, sections 8 and 9). The plan is turned half round, as
plans are, the street at the bottom, so each room faces the other way from its picture. A click
on a room the family has been in takes the one being played there, the other two coming along
and arriving as they would by the stairs, a door or the ladder. The study is there to go to only
once it has been opened and walked into, and the living room does not let them go by the map
once they have left for Nevada (`home.left`). A click on a sister's portrait on the plan is
playing as her, as her portrait in the team bar is.

**What moves (round four).** Nothing that moves by nature is painted still any more: in the
Retreat the little fountain on the sound table runs (a thread of water off the bamboo
spout, rings on its pool), the flameless candles' little lights flicker, and the diffuser
breathes out a soft mist; in Little Sister's room the mobile of felt chickens stirs, each
chicken swinging a little on its thread. None of it is a thing to click, and nothing about
the puzzles changed. (Nobody but the family is in the house, so nobody else walks about.)

## Cut-scenes and puzzles

```
Cut-Scene: Voicemail, for the ninth time (and a prayer)        (opens the act)
```
The living room. A phone rings out and goes to voicemail: "You've reached Dad. I'm
either driving or lost. And I am never lost." Mom has now called nine times. Little
Sister: "Daddy's not lost. Daddy's EARLY." Big Sister does the arithmetic on a
four-hour drive. Dinner was at six, five places are set, and Mom is not clearing two of
them away. Then: "First things first, girls." She prays, in two lines of her own:
"Father, You know where they are tonight, and I do not. Keep them. And bring us to
them. In Jesus' name." Little Sister adds a postscript: "And please make Daddy ask for
directions. Just ONE time. Amen." Big Sister remembers that Dad's phone still reports
to the family computer, "the mainframe", which is upstairs in his study, and that the
internet has been down since Dad "improved" the wiring. Mom says where the router
lives (the closet under the stairs, next to the vacuum cleaner), and turns stage
manager: "Places, girls. We are going to find out where that phone was last seen."
*Plants:* "Daddy's EARLY" (pays off in "Some when", in the middle of Act Four). That Dad never asks for
directions (#7; and Little Sister has now prayed that he will). The study, the computer
and the router (#1 to #7). "Places, girls."
*Notes:* the old cut-scene's lines are kept and in their old order. All three bow their
heads for the prayer (`actor.pray`, when the pose exists).

```
Puzzle #1: The Other Eighty-Eight        (Home · Lead: Big Sister or Mom · the landing, or the piano)
Needs:        nothing
Setup:        Dad's study is locked. Taped to its door, in his capitals: "TRIP HEADQUARTERS. AUTHORIZED
              PERSONNEL ONLY. LOST YOUR KEY? IT IS WITH THE OTHER EIGHTY-EIGHT. - THE MANAGEMENT". The first
              time they come upstairs Big Sister points at it, and Mom says: "With your father there is
              always a notice."
Wrong tries:  The study door            -> "Locked. Naturally. And he's left us a notice instead of a key."
              Little Sister reads it    -> "Eighty-eight keys! Daddy has a LOT of doors."
              The key bowl on the hall table -> every key this family owns, except the two Mom wants tonight.
Solution:     Big Sister or Mom reads the notice (it is shown close up). Big Sister: "Eighty-eight of what?
              ...Keys. Fun fact: a standard piano has eighty-eight keys. Dad has hidden the study key in the
              piano." Mom: "He has hidden a key in MY piano." (If it is Mom who reads it: "A matter of
              record: a full-size piano has eighty-eight keys." and Big Sister was half a second behind.)
              OR, from the other end, before anyone has read it: Mom or Big Sister plays the piano
              downstairs, and one note goes thunk. "Something is lying on the hammers."
Gives:        The knowledge that something is in the piano (`home.keyInPiano`).
Plants/pays:  Plants "THE MANAGEMENT" (the vault's label, and the card inside it). If they found the dead
              note first, reading the notice afterwards joins the two up: "So THAT is what is lying on
              the hammers."
Notes:        A piano has eighty-eight keys: a fact Mom and Big Sister both have, and Little Sister has
              not. The hint from each says the notice is a riddle; Little Sister's says it wants
              somebody who likes words.
```

```
Puzzle #2: The Key In The Piano        (Home · Lead: Little Sister · the living room)
Needs:        #1
Setup:        The key is down inside Mom's upright piano, on the hammers, under the A above middle C.
Wrong tries:  Mom at the piano          -> she lifts the lid and can SEE it, with a tag on it in Dad's
                                           capitals. "And I cannot reach it. My arms are a civilized length."
                                           "The panel down by the pedals lifts off. Under the keyboard,
                                           sweetheart: that is your cue."
              Big Sister at the piano   -> "It is under the A above middle C. I can hear exactly where."
                                           "I am not putting my arm in a piano. I need all ten fingers. I
                                           am halfway through a sonata."
              Mom asks Big Sister       -> "It is a piano, Mother, not a mailbox. Ask the one who fits
                                           under things."
Solution:     Play as Little Sister and use the piano. "I FIT!" She goes under the keyboard, takes the
              panel by the pedals off, and comes out with a marble, a penny and a key.
Gives:        The study key (tagged "TRIP HQ"). The piano's lower panel stays off from now on.
Plants/pays:  "I FIT!" is hers, and belongs here as much as at the closet (#5); in Act Four she eyes
              the fence the same way.
Notes:        "He hid it in a piano, and then he labelled it." Whoever is standing at the piano makes
              room for her. Once the key is out the piano is a piano again: Big Sister plays her phrase
              in a minor key, Little Sister plays "Plonk", and Mom, who would not play before, plays a
              hymn she names ("A Mighty Fortress Is Our God"), quietly, for courage, and says the first
              verse of the psalm behind it (Psalm 46:1).
```

```
Puzzle #3: Open Trip Headquarters        (Home · Lead: whoever holds the key · the landing)
Needs:        #2
Setup:        Little Sister has the key. It can be handed to either of the others.
Wrong tries:  The study door, as one who is not holding the key -> she says who is. Mom: "Your little
              sister is holding the key. She fetched it, so she gets to turn it." Big Sister: "Mom has
              the key. Technically she outranks the Management."
              The key on the Son's door -> "It doesn't have a keyhole! It has a PASSWORD."
              The key on the front door -> "This door wants a car at the other end of it."
Solution:     As whoever holds the key, use the study door (the key in her pockets is enough; using
              the key on the door does the same). Mom: "'Authorized personnel only.' I authorized
              myself on our wedding day." They all go in.
Gives:        The study. From now on its door is the way into `home-study`.
Plants/pays:  Plants handing things over, which #6 and #8 use, and Act Four's coin depends on.
Notes:        The first time in: Mom, "He hasn't let me dust in here since March."; Big Sister
              points out the computer and the "family vault"; Little Sister: "Something's BLINKING!"
              (the answering machine: #8).
```

```
Puzzle #4: The Retreat Goes Dark        (Home · Lead: Little Sister, then Big Sister · her fort, and the attic)
Needs:        nothing
Setup:        The closet under the stairs is too dark to find a plug in (#5), and Little Sister will not
              go in without her own flashlight. It lives just inside her blanket fort, in her room,
              where nobody but she may go: "NO BIG SISTERS" is her sign, and her rule.
Wrong tries:  Mom or Big Sister at the fort, or at the flashlight -> "You don't go into a lady's fort
                                             without an invitation." / "'NO BIG SISTERS.' I respect a posted
                                             boundary."
              A dead flashlight at the closet -> "A DEAD flashlight is just a pink stick! It wants
                                             batteries. THEN I go in. That's the plan."
              Big Sister at her sound machine, before there is a dead flashlight in the house -> "It
                                             stays on. Tonight of all nights. It is the only one of us
                                             that is calm."
              Mom at the sound machine     -> "The batteries are in there, and they're not mine to take.
                                             Not from a daughter. Your sister has to do this herself."
              Little Sister at the sound machine -> "The batteries are IN there! I can't touch it: rule
                                             AND treaty. So YOU have to. It's your music box. Go on."
Solution:     Little Sister fetches her flashlight from the fort. "CLICK. ...Click? CLICK CLICK CLICK."
              "It's DEAD. I used it all up last night. I was reading to the flock under the blanket.
              They wanted the WHOLE book." Mom has not seen a battery of that size in the house since
              Easter. Big Sister, unasked: "...There are four. In my sound machine. In the Retreat. I
              should like it noted that I said so myself." Up the attic ladder. As Big Sister, open the
              sound machine: "Very well. The Retreat goes dark so that the internet may live." The music
              stops. Then batteries and flashlight have to meet in one pair of hands: whoever holds one
              is handed the other, and puts them in. (If Big Sister is holding the flashlight herself
              when she takes them, in they go.)
Gives:        A flashlight that works (`home.flashWorks`). The Retreat is quiet for the rest of the act.
Plants/pays:  Pays off handing things over. Plants the sacrifice: "I intend to mention this again."
              ("You will, darling. Often. And every time, I'll say thank you and mean it.")
Notes:        Little Sister: "IT STOPPED. ...Now I can hear the water. It's going tick, tick, tick."
              The fountain sounds like a clock, which Big Sister had been managing not to notice. She
              can fetch the flashlight before she has ever tried the closet. Whoever goes to the fort,
              the bed or the sound table has it to herself: the other two step back and watch. A beat's
              hint is one line for each of them, whatever has been done so far, so these three are
              worded to be true at every stage: a dead flashlight wants batteries, the only ones live in
              the sound machine, and then the two must meet.
```

```
Puzzle #5: Plug In The Router        (Home · Lead: Little Sister · the closet under the stairs)
Needs:        #4 to finish it. (She can try the closet from the first line, and that is how #4 begins.)
Setup:        Dad "improved" the wiring this morning, and the internet has been down since. The router
              is in the closet under the stairs: a low door that stops at Mom's shoulder and opens four
              inches. A tiny red light shows in the gap.
Wrong tries:  Mom at the closet           -> "A lady does not squeeze into closets, darling. A lady has
                                             a seven-year-old."
              Big Sister at the closet    -> "I refuse. There are spiders in there, and I am thirteen.
                                             Both of those are final."
              Little Sister, with no light -> "I FIT!" She goes in. "It's SO dark. I can't find the plug.
                                             I found the vacuum. With my NOSE." She comes out: "I need
                                             my flashlight. MINE. The pink one, from my fort. Come ON,
                                             everybody. I know the way!" She will not go in again
                                             without it: "Not without my flashlight! I'm not scared.
                                             I'm BRAVE-scared. Brave-scared people bring a flashlight."
              Little Sister, when one of the others is holding it -> "I need my flashlight BACK.
                                             Somebody's got it who isn't me. Hand it over, please.
                                             I'm the closet person."
              The computer upstairs, before this is done -> "No internet."
Solution:     With her flashlight working (#4), Little Sister goes into the closet. "Flashlight ON!
              Hi, vacuum. Hi, spiders. And there's a plug that isn't plugged into ANYTHING!" Mom
              talks her through the socket. The little light goes from red to green.
Gives:        The internet. The computer upstairs can be signed in to.
Plants/pays:  "I FIT!" again. The flashlight goes with her to Nevada (where, in full morning sun, its
              little spot cannot even be seen).
Notes:        "I'm a ENGINEER!" "AN engineer." "That's what I SAID." The other two stand clear of the
              closet door to watch. While she is in there with it, its glow shows in the gap.
```

```
Puzzle #6: Read Dad's Note        (Home · Lead: Big Sister · the study)
Needs:        #3
Setup:        The computer wants a four-figure password. There is a yellow note stuck to the monitor,
              in Dad's handwriting: "Password: the year of the best thing since." He has left off the end.
Wrong tries:  Mom reads the note          -> "Since WHAT, my love?"
              Little Sister reads it      -> she can read "PASS WORD", and admires the loopy Ys.
              Little Sister at the sign-in page (if the router is on) -> she types 1, 2, 3, 4. "It said no AGAIN."
              Mom or Little Sister takes the note -> it goes in her pocket. Looking at it there: "Your sister
                                             will know. She knows the year of everything."
Solution:     Get the note in front of Big Sister: she takes it herself, or whoever has it hands it to
              her (in any room). "Since sliced bread. With Dad, everything is the best thing since
              sliced bread. Fun fact: sliced bread was first sold on the seventh of July, 1928, in
              Chillicothe, Missouri. The password is 1928."
Gives:        The password.
Plants/pays:  Pays off #3 (handing things over).
Notes:        Exactly as in the first version of the act, moved upstairs. The fact is true and has
              been checked. The hint is on the note and not on the screen, so this does not wait for #5.
```

```
Puzzle #7: Answer The Question        (Home · Lead: Mom · the study)
Needs:        #5 and #6
Setup:        With the router on and the password known, anyone can sign in. Then the computer asks one
              more thing, because it has not seen this sign-in before: "What did you promise on your
              wedding day?"
Wrong tries:  Big Sister signs in         -> "I was not invited to the wedding. Mother?"
              Little Sister signs in      -> "I wasn't BORN. Mommy!"
              Mom: "To love, honor and cherish."         -> "No? I did say that. I had hoped he was listening."
              Mom: "To always take the scenic route."    -> "No. That was not a promise. That was a warning."
Solution:     Mom: "To never ask for directions." The map comes up: one dot. "Dad's phone. Last seen
              5:47 p.m. Thirty-seven miles past Last Gas." In the middle of Nevada.
Gives:        The place (`home.foundPing`).
Plants/pays:  Pays off the voicemail, Little Sister's postscript to the prayer, and the wedding
              photograph on the landing ("He was forty minutes late for it. He had refused to ask the
              way."). Plants the place name for Act Four.
Notes:        "He promised me he would never ask for directions. It is the one promise he has always kept."
              A wrong answer costs nothing but a line. If they have already heard the message (#9),
              Big Sister does the sum here: "5:47. His message was at 5:41. Six minutes after that, his
              phone stops."
```

```
Puzzle #8: Wind The Tape        (Home · Lead: Mom · the study; the pencil is in the living room)
Needs:        #3
Setup:        Dad will not replace his answering machine. Its little red light is blinking: one new
              message. And a loop of its tape is hanging out (Little Sister "fixed" it last week).
Wrong tries:  Little Sister at the machine -> "I'm not allowed to fix it again. Mommy said. With her
                                              whole-name voice."
              Big Sister at the machine    -> "Fun fact: you can wind a cassette by turning its hub with
                                              a pencil. Mine are too slim. Dad's is not." And with the
                                              pencil in her hand: "I know that it fits. I do not know
                                              how hard to turn. That tape is his voice. Mom should do this."
              Mom, with no pencil          -> "It wants winding back in, and for that I want a pencil."
                                              "There's exactly one pencil in this house that can ever
                                              be found. It's on your father's crossword."
              Big Sister's own pencils (her desk, in the Retreat) -> the slim kind. Not for this.
Solution:     Fetch Dad's pencil from his crossword, on the arm of his chair in the living room (any of
              them can take it), get it to Mom, and have Mom use the machine. "I recorded entire
              musicals off the radio with one of these. Pencil in the hub, and gently."
Gives:        A machine that will play (`home.tapeWound`). The loop of tape is gone from the picture.
Plants/pays:  Pays off handing things over. Plants the message.
Notes:        Mom is of the generation that did this. Big Sister has the fact and not the knack. If
              one of the girls is holding the pencil when the machine is tried, she says so.
```

```
Puzzle #9: Play The Message        (Home · Lead: any of them · the study)
Needs:        #8
Setup:        One new message.
Solution:     Any of them presses play. The other two come and stand to listen. Dad, cheerful: "Hi,
              honey. It's 5:41 and we are making GREAT time. I found a shortcut." "Thirty-seven miles
              past the last gas station and not one other car. The boy says hi." "He says the road
              sign up ahead looks funny. ...Huh. That IS funny." "That sign just changed its--" And
              the tape hisses.
Gives:        Dad's last message (`home.heardMessage`). The machine's light stops blinking.
Plants/pays:  This is the moment the player saw in the opening of the game. Act Four's witness says
              "The road sign changed its mind."
Notes:        Little Sister: "Changed its WHAT? Daddy! Changed its WHAT?" Big Sister does the
              arithmetic: with the dot already found, "5:41 on the tape. His phone was last seen at
              5:47. Whatever happened took six minutes."; without it, she writes down the minute. Mom:
              "I do not need to hear it twice. He sounded happy." Nobody plays it a second time.
```

```
Puzzle #10: We The People        (Home · Lead: Mom · the study; the clue is in the living room)
Needs:        #3
Setup:        Mom's car keys left the house this morning in Dad's pocket (the front door says so the
              first time anyone tries to leave). The spare is in the "family vault": a cash box with a
              dial, on the study shelves. Its label, in Dad's hand: "FAMILY VAULT. Combination: the
              year WE THE PEOPLE got it in writing. Your mother will know. She brings it up."
Wrong tries:  Big Sister reads the label  -> "I can think of three years. Mom will know which."
              Little Sister reads it      -> "MOMMY! The box says you know!"
              Mom: "Seventeen seventy-six." -> "No. 1776 is the Declaration, the Fourth of July. 'We
                                               the People' came later."
              Mom: "Seventeen eighty-nine." -> "No. In 1789 the new government began, and General
                                               Washington took the oath. It was written by then."
              Mom: "Let me think about it." -> she leaves the dial alone.
              The study key on the vault  -> "The vault has a dial, not a keyhole."
Solution:     Mom: "Seventeen eighty-seven." "Signed in Philadelphia on the seventeenth of September.
              He does listen. Just not at the time." Inside: her spare car key, two ketchup packets,
              and a card: "KNEW YOU'D KNOW. - THE MANAGEMENT."
Gives:        The spare car key (`home.hasCarKey`).
Plants/pays:  The clue is in the house for a player who does not know: the framed Preamble in the
              living room. Mom, looking at it: "'We the People.' Signed in Philadelphia, the
              seventeenth of September, 1787. It still gives me goosebumps." Pays off "THE MANAGEMENT". The ketchup
              is Dad's running gag (he is saving it; nobody has asked for what).
Notes:        The wrong years cost a line each, and each line is true. "He keeps ketchup in a vault."
```

```
Puzzle #11: Leave For Nevada        (Home · Lead: any of them · the front door)       THE GATE
Needs:        #7, #9 and #10
Setup:        Nothing stops them now.
Wrong tries:  The door, with no dot on the map: Mom -> "Not until we know where we are going. One of us
              in this family must." Big Sister -> "A journey without a destination is just Dad."
              Little Sister -> "I'm READY. I've been ready since dinner. ...Which way IS Daddy?" (The
              first time, Mom adds why they will want a key: "And there's the matter of my car. Your
              father moved it this morning. My keys left in his pocket." Big Sister: the spare is in
              the family vault. Little Sister: "It's a box with a clicky wheel! Mommy will know the
              clicks.")
              The door, with the dot and no message: Mom -> "There's a message on your father's
              machine upstairs, and I want to hear it first."
              The door, with both and no key: Big Sister -> "Destination: yes. Message: yes. Car key:
              no. Two out of three does not start an engine."
Solution:     Open the door. Mom: "One moment. In this family nobody starts a journey without the
              psalm." Big Sister: "Psalm 121, verse 8. She always does this part." Little Sister, by heart: "The LORD shall
              preserve thy going out and thy coming in from this time forth, and even for evermore."
              Mom: "Amen. Going out, and coming in. All five of us." Then, as before: "Coats, girls.
              We are going to Nevada." "We are going to be perfectly polite, and completely impossible
              to get rid of."
Gives:        Act Four.
Notes:        The drive is a card ("The Middle of Nevada. The next morning."). As they leave, the
              other two turn to whoever is at the door. Whoever holds the car key, it is Mom who drives.
```

Also in the house, for character and nothing else. Each of the three has her own line
for every one of these, and they have things to say to each other in every room.

- **The Son's door** (the landing). It says NO GIRLS ALLOWED ("He spelled all three
  words correctly this year. I was so proud that I very nearly obeyed it."), and it is
  booby-trapped. His toy alarm asks for the password in his own recorded voice ("HALT!
  This is Operation No Girls. What's the password?"). Little Sister knows it, because she
  has watched him, and does the voice: "The password is: I still want a dog." It says
  CORRECT, ten out of ten. Big Sister declines to guess, and simply opens the door.
  Either way, when a sister opens it, his toy blaster, hidden in the slot over the door,
  fires a volley of seven foam darts, orange and blue (drawn live, a "thwip" each), which
  come down on the runner in front of the door and stay there. Big Sister says the
  author's line: "I don't want to go in there. The rug is probably booby-trapped."
  Little Sister, if it was her: "It said CORRECT! You can't say ten out of ten and then
  SHOOT people! ...It was a GOOD trap, though." If it was her sister: "He GOT you! SEVEN
  darts! ...Right. I'm making a sign for MY door. NO BROTHERS. Except on Saturdays."
  Mom does not try his door tonight ("'NO GIRLS ALLOWED.' I'm his mother, which he's
  always counted as a separate thing. ...Not tonight."); when the darts have come down
  she says, quietly, "Not tonight, sweetheart (darling). I am not ready to look at that
  room with nobody in it." The second time either sister tries it, one more dart, the
  one he kept back, flops out at her feet: "ONE more! He saved one for me! ...That's not
  a trap anymore. That's just RUDE." / "One more. He kept one in reserve. I respect that,
  and I am still not going in." After that the trap is spent and nobody tries: Little
  Sister can wait ("I'm getting good at it"), and Big Sister stands by what she said
  about the rug. The darts lie on the runner for the rest of the act (Mom leaves them
  where they fell, for him to count). The door stays shut all act. It is still the one
  place the act is allowed to be sad.
- **The railing**: the living room, seen from above. "A set with the lights left on and
  nobody on it. Two of the cast are late."
- **The family Bible**, at the head of the table by Dad's plate, open where he left it
  this morning at the psalm for a journey. Mom has verse 2 of Psalm 121, Big Sister
  verse 1, and Little Sister knows Psalm 23:1 by heart, and adds what she wants: "...I
  do want Daddy, though."
- **The sampler** over the front door (Joshua 24:15) and **the framed Preamble**.
- **Mom's bookcase**: the Adams letters, General Washington, Dr. Franklin, a great many
  plays, and the hymnal. Abigail Adams's "Remember the Ladies".
- **Little Sister's room**, which is all chickens. The flock ("Admiral Doodle on top.
  Corporal Speckle. Private Peep. Each has a name, a rank and a job. I know them all.
  Against my will."); the chart, MY CHICKENS, twelve of them, the General with a star
  ("You go up a rank every time you go in the wash."); the tea party; the hen house that
  was a dollhouse ("Everybody in my hen house is home. I checked. Twice."); the pillow
  with one place kept on it, RESERVED, for General Feathers, who is on the trip in
  Daddy's suitcase ("I'm not worried about the General. I'm a LITTLE worried about
  Daddy. That's why I SENT her."). It is where **"Chickens KNOW."** is first said, of
  the flock, as a plain fact: it pays off in every other act. And at the nest Mom says
  the truest thing in the room, once, half to herself: "'...even as a hen gathereth her
  chickens under her wings'..." "Tonight I know just how the hen feels." (Matthew 23:37:
  since round seventeen she says the words and not the reference.)
- **The Retreat.** Little Sister takes her boots off with great ceremony and whispers
  at full volume ("THIS IS MY WHISPER."). Mom: "Soft light, one sound, nothing out of
  place. Darling, it is a set. It is a very good set." She can name the key the music
  is in (D major). The rules, close up: THE RETREAT. 1. SHOES OFF. 2. VOICES DOWN. 3. NO
  CHICKENS; and under the third, in crayon, AN APPEAL HAS BEEN LODGED. ("You haven't
  made a room. You've founded a republic.") The room is perfectly calm and Big Sister
  is not: she has counted the little lights in fours, twice.
- **Big Sister's timeline**, on the Retreat's wall: where the game says how it counts
  the years. "I used Archbishop Ussher's dates. He counted the years from the Bible's
  own genealogies." The first time any of them looks along it they read it between
  them: 4004 B.C., the Creation; 2348 B.C., the Flood; 1921 B.C., Abram leaves Haran
  and goes down into Egypt; 1491 B.C., the Exodus; 44 B.C., the Ides of March; and at
  the red mark, what B.C. and A.D. mean. Mom's matter of record is that the
  Archbishop's book was published in 1650. Little Sister: "There's not much paper
  before Abram! I thought the beginning would be the LONGEST bit." Big Sister: "It is
  as long as it was." Nothing else is said about the dates, here or anywhere. Little
  Sister is on the timeline, at the far end, in pencil. (1921 and 44 are the two numbers
  on the notice in Act Four.)
- **The wall map**, **the corkboard** and **the banner** in the study: Dad's route in
  red wool, and a shorter piece, in yellow, across a part of the map with nothing on it
  ("Yellow is for caution. He chose it himself."); the Son's "Operation Road Trip",
  whose steps one to five are "snacks"; TRIP in Dad's blue, and HEADQUARTERS in the
  Son's hand, one color to a letter.
- The clock, the kitchen (her best hen is on the fridge, guarding the snacks), the
  photographs (the lake; the wedding), the stairs (sixteen steps: Big Sister has
  counted), the coat hooks, the hall table's key bowl, the countdown to the trip, the
  Son's school bag, the laundry hamper, the globe, the model biplane, the shelves of
  manuals read halfway, the things that did not fit in the car ("He left the maps."),
  Dad's armchair and his crossword.

---

# Act Four: The Last Stop Before Nothing

The middle of Nevada, the next morning. "GRANDPA JOE'S LAST STOP. GAS (crossed out). ROCKS.
LEMONADE."

<!-- NEVADA-12W: Act Four as expanded in round twelve. The old part of this document (puzzles #5 to #9 and the two
cut-scenes) is kept, word for word where the act kept it; what changed is said where it changed. -->
<!-- PASS-17N: round seventeen's dialogue pass (16 October). Where this act's cards and the ledger quote a line the pass
changed, the quotation is the new line (Act Four but the letterbox, #12 and #13, which are LETTER-17's; and Act Five).
Every change, before and after, is in the pass's record, changes.json, and its summary, changes.md. -->
**Round twelve (10-12 October): Nevada, expanded.** The author's words of 9 October: the old
man at the Last Stop is Grandpa Joe, with a pet raccoon called Ranger, a rocking chair, a banjo
and a Southern accent; the store gets an inside, a run-down gas-stop convenience store, with
puzzles made of things in it; his wife is Grandma Jolene, kooky and zany, who bonds with Little
Sister over chickens; after the family goes into the door, the gray suit, Jed, makes a call and
Grandpa Joe hits him over the head with the banjo; four gray suits come in a limousine and take
Grandpa Joe away, and Ranger follows; and then Grandpa Joe and Ranger are played. On 10 October:
the letterbox (the Son on the other side of the coin door), and dialogue that is part of the
puzzles, the way the classic games do it. Every puzzle the act had is kept (#5 to #9). #5 is a
dialogue tree now. Four puzzles are new (#10 to #13), made of things from the store, and the
act's gate is the walk through the door (#13), not the coin. The design is
`briefs/out/nevada-expansion-design.md`, with its thirteen decisions taken as
`briefs/NEVADA-12.md` says; the lines are `js/content/lines/nevada.en.js` and `limo.en.js`, and
the talks are trees in `js/content/talk/nevada.js`. All of it is built (12 October): the roadside
(`js/content/scenes/nevada-roadside.js`), the store inside (`nevada-store.js`), the cut-scene
"Backup" (`js/content/cutscenes/backup.js`) and the limousine (`nevada-limo.js`). What follows is
the act as the game plays it. Where the builders chose something the design left open, or staged it
otherwise, the card says so; what is left for the author to decide is listed in
[DESIGN.md](DESIGN.md), section 14. The author will play it and review every puzzle.

## Characters

- GRANDPA JOE (he was the old-timer): sells rocks and lemonade from a rocking chair in front of his porch, with a banjo across his knees and his raccoon sitting beside the chair; saw the low sun flash off the wagon and the sky open where the flash fell, and has told everyone he saw nothing; wants to be asked nicely. Slow and Southern, and the kinder he is the slower he talks.
- GRANDMA JOLENE: his wife, behind the counter of the store under a different hat every visit; certain, cheerful and wrong about every fact, and right about every person; her five hens have quit laying and stand facing the fence; wants her girls to lay again, and will not sell the sun shade in her window.
- RANGER: Grandpa Joe's raccoon; never says a word ("..."), and Grandpa Joe says what he means; does not steal, trades; has the coin, in his basket under the store's counter.
- JED, THE MAN IN GRAY: stands in front of the notice; can neither confirm nor deny the fence, a dog, General Washington or a cheeseburger; has not had a snack since 0500. Little Sister named him Mister Gray. The family never hears his name.
- THE BACKUP: four men in gray suits, black sunglasses and earpieces, in one gray limousine; say sir to everybody, apologize while they do things, and follow regulations to the letter.
- HOUSTON: a voice in Jed's earpiece. Dispatch. "Houston, we have a problem" is her name.
- THE HENS: Darlene, Charlene, Marlene, Arlene and Doreen, out back in a row, facing the fence. "Named for my sisters. The hens are nicer."
- MOM, BIG SISTER, LITTLE SISTER: as before, with lemonade, and with the five things from the house still in their pockets. None of those is needed here.

Their pages are in [CHARACTERS.md](CHARACTERS.md), under "The Last Stop, and the men in gray".

## Puzzle structure

```
                        Cut-scene: Where the map stops
                                      |
      +-------------------------------+-------------------------------+
      |                               |                               |
 #5 Ask Nicely (Mom; a talk)  #7 Two Hundred Questions        #11 Jolene's Girls
   -> Grandpa Joe's story       (Little Sister) -> Jed             (Little Sister, out back)
   -> "Ranger had it"                 |                          -> the run of the store
      |                      #8 Read The Notice                    (the sun shade is hers to give)
 #10 Ranger's Trade              (Big Sister)                            |
   (Big Sister, with mirror           |                                  |
    shades Mom bought) -> the coin    |                                  |
      |                               |                                  |
 #6 Hand Over The Coin                |                                  |
   (Big Sister reads it, there        |                                  |
    and then)                         |                                  |
      +---------------+---------------+                                  |
                      |                                                  |
   #9 Flash The Coin Where The Tracks Stop (whoever holds it; a prayer first)
                      |  -> a door the size of a coin
            Cut-scene: Some when (as it was; then her head in the hole, and Big Sister's rule)
                      |
            The letterbox: the Son, on the other side of the coin door
                      |                                                  |
   #12 Something That Shines Like A Station Wagon  <---------------------+
       (Big Sister has the rule; the banjo is a half-answer;
        the sun shade from the window; Grandpa Joe holds it)
                      |  -> a door as wide as a windshield
   #13 Going Out And Coming In (the gate: the family walks in)
                      |
            Cut-scene: Backup (Jed, the banjo, the limousine)
                      |
   ACT FIVE opens: Everybody's Grandpa (Grandpa Joe and Ranger, in the limousine)
```

Goal of the act, now: **find out what happened to them, and go after them.** Chain A (the
witness, the raccoon, the coin) and chain B (Jed, the notice) are the act as it was, with one
more puzzle in A: the coin has a raccoon between it and the family. Chain C (the hens) is new
and open from the first line; it is Little Sister's, and it is the one that makes the Last Stop a
place rather than a counter. #9 is still the act's middle: a coin's worth of light, a coin's
worth of door, and the scene "Some when" as it was. Then the act goes on: the door is too small,
and the three things the family has learned (the old man's flash, the newness of the coin, and
the size of the door) add up to one more puzzle, which is the store's. The gate is the walk
through.

The beats (`js/content/acts/nevada.js`), each with the fact it makes true: `nevada.arrive` (the
opening, `nevada.arrived`), `nevada.witness` (#5, `nevada.witness`), `nevada.ranger` (#10,
`nevada.traded`), `nevada.coin` (#6, `nevada.coinRead`), `nevada.distract` (#7,
`nevada.distracted`), `nevada.notice` (#8, `nevada.notice`), `nevada.hens` (#11, in the store,
`nevada.jolene`), `nevada.tracks` (#9, `nevada.doorOpen`: no longer the gate), `nevada.letterbox`
(`nevada.heardSon`), `nevada.shade` (#12, `nevada.wideOpen`: it needs `nevada.doorOpen`,
`nevada.jolene` and `nevada.heardSon`) and the gate, `nevada.through` (#13, `nevada.left`). Act
Five's (`js/content/acts/limo.js`) begin where this act ends, on the roadside: `nevada.backup` (the
cut-scene, `nevada.backup`); then, in the limousine, `limo.arrive` (its opening, `limo.arrived`),
`limo.ropes` (#14, `limo.loose`), `limo.bag` (#15, `limo.map`) and the gate, `limo.end`
(`limo.done`: the end of the demo).

| | What only she can do | In Act Four |
| --- | --- | --- |
| **Mom** | Adults listen to her; she knows her husband and his car | Gets Grandpa Joe to talk (#5); buys what the store sells (the mirror shades, three waters); is the one Grandpa Joe will play for, and hold a light for |
| **Big Sister** | Remembers the fact | Reads the coin (#6) and the notice (#8); knows how a raccoon feels a thing, and trades (#10); pins the Son's year through the door; works out the rule of the doors (#12) |
| **Little Sister** | Fits, distracts anybody, and knows chickens | Asks Jed two hundred questions (#7); is the only one Grandma Jolene's hens will listen to (#11); posts a penny to her brother |

**The rule of the doors**, the same in every era (it is Act One's and Act Two's, and is
written out in [PUZZLES-rome.md](PUZZLES-rome.md)): a door in time stays where it once
opened, shut and invisible, and it hums. Light thrown on the place opens it, and the
more light, the bigger the door. Dad learns it in the pyramid with a flashlight and a
sunbeam. The Son learns half of it in Rome with a coin. Mom and the girls are never
told it. They have an old man who saw the low sun flash off the wagon and the sky open
where the flash fell, and does not know which part of his story matters; a hum, where
there is nothing to hum; a low morning sun; and a coin so new it shines. In this act they
learn all of it by doing it: a coin's worth of door, then a banjo's, then a windshield's.

## Location layout

Three scenes now: the roadside as painted (the shack's end repainted), the store inside (new),
and the limousine inside (new, Act Five's). The store and the roadside are one era (no card
between them), and the three of them go in and out of the store together.

```
THE ROADSIDE (nevada-roadside), as painted, the shack's end repainted:
+------------------------------------------------------------------------------------+
| the SIGN: GAS        GRANDPA JOE'S                  mesas, far off                 |
| (crossed out),       LAST STOP (a new board                                        |
| ROCKS, LEMONADE      nailed over the old one)                                      |
|                                                                                    |
| the road     THE SHACK, the store: its     the gas  LEMONADE   the FENCE ........  |
|              PORCH, the shop's DOOR (the   pump     STAND      the NOTICE, and JED |
|              way in), Jolene's spare HAT            (umbrella) in front of it, or  |
|              on a nail in the porch post                       backed off along    |
|                                                                the fence           |
|                      GRANDPA JOE in his ROCKING CHAIR, on                          |
|                      the ground in front of the porch, the                         |
|                      BANJO across his knees; RANGER on the     the tire tracks run |
| MOM'S CAR            ground beside the chair                   out from under the  |
|                                                                fence and stop at   |
|  Here: Mom, Big Sister, Little Sister                          THE GLASS. It hums. |
+------------------------------------------------------------------------------------+
```

The shack has a second board nailed up over LAST STOP, in the same hand, that says GRANDPA JOE'S;
a door that reads as a door (a chrome pull, its edge lit), which is the way into the store
(`store`, "Go into"); and Jolene's spare hat, a straw sun hat with a blue scarf, on a nail in the
porch post beside it. The lawn chair has gone. Grandpa Joe's rocking chair is drawn with him, and
stands on the ground in front of the porch, where the lawn chair stood, between the gas pump and
the lemonade stand (the design put it up on the porch boards: see DESIGN.md, section 14). He gets
up out of it slowly, to pour lemonade at the stand, to play at the glass and to hold the sun shade,
and sits down again; and now and then, by himself, he gets up and takes a few steps, toward the
pump or out to look down the road, a hand to the small of his back. His chair stays where it is
while he is up. Ranger sits up on the ground beside the chair, on our side of it, and now and then
goes over to the lemonade stand to wash a pebble. Everything else (the stand, the pump, the fence,
the notice, the tracks and the glass) is where it was, and there is still no way out at the edges
of the picture. Coming out of the store, the one leading stands on the porch at the shop's door and
the other two just outside it.

```
THE STORE (nevada-store), new: one painting, the camera just inside the front door, looking along the store:
+--------------------------------------------------------------------------------------------+
|                 THE HUBCAP WALL, high round the walls (a hundred and twelve)               |
|                         THE CEILING FAN (still since 1979)                                 |
| THE      THE FRONT     the TV, on the  THE BULLETIN   THE HAT RACK: a     THE BACK DOOR,   |
| FRONT    WINDOW, and   SURVIVAL SHELF; BOARD (lost    peg for each hat;   open: THE HEN    |
| DOOR     in it THE     HAROLD, the     dogs, and      today's is on her   YARD, five hens  |
| (Bernice SUN SHADE,    COOLER          "JED: NO       head                in a row, facing |
| over it) DISPLAY ONLY                  CHEESEBURGERS.                     the fence        |
|                                        WE TOLD YOU.")                     THE PAY PHONE    |
| THE AUTO THE SPINNER   THE COUNTER: GRANDMA JOLENE behind it; the          JOLENE'S CHAIR  |
| SHELF    RACK (one     POSTCARDS, the PICKLED EGGS, the TAKE-A-PENNY      (her knitting)   |
|          pair of       dish, the REGISTER, the MAP RACK; RANGER'S                          |
|          MIRROR        BASKET under its near end; the GRILL and the       THE ROCK BINS    |
|          SHADES left)  HOT DOG ROLLER at its far end                      (ROCKS $1)       |
|  Here: Mom, Big Sister, Little Sister, just inside the door                                |
+--------------------------------------------------------------------------------------------+
```

One painting, through one camera, as the house's rooms are painted: the front wall, with the
window and the front door, is the left of the picture, and the back wall runs across it with
Harold in its left corner, the counter in the middle and the back door at its right. Every one of
these is a thing to click, and each of the three has a line for each (below, "Also in the store").
Grandma Jolene stands behind the counter under the hat of the visit (her other four hang on the
rack over it, with a gap for the one she has on) and now and then goes along to the register and
back. The hen yard is seen through the open back door, a step down: the five hens are in the
picture, with their backs to us, and Little Sister can go out to them onto the step (the yard is
not a scene of its own). The other two watch from the doorway. The way out is the front door, at
the left edge, and its bell, Bernice, rings as they come in and go out.

<!-- MAP-15D -->
**The front door, and the map (round fifteen).** As the three leave the store, by its front door
or by the map, they are not inside any more (`nevada.inStore` false), so the next time they come
in is a new visit, and Jolene is under her next hat. That is done by the store's `leaving` now,
which runs however they leave; the front door only rings Bernice and goes. Coming in by the map
is a visit like any other: Bernice rings, and Jolene says hello. The Map button (or M) shows
Grandpa Joe's own road map from the rack on his counter, opened flat: the highway through LAST
GAS, "37 MI." on to the Last Stop and TO NOTHING, and in its detail panel the lot in plan, with
the store drawn inside the shack's walls and the hens out back (DESIGN.md, sections 8 and 9). A
click on the lot or the store takes the three there by the one short way between, the shop's
door. Neither lets them go by the map once the family has gone through (`nevada.left`), and
nobody leaves the limousine by it: Grandpa Joe is belted in. Grandpa Joe and Ranger have no
portrait at the Last Stop in Act Four (they are its people); from Act Five theirs are on the
road beyond it, with a small printed limousine.

```
THE LIMOUSINE (nevada-limo), new, Act Five's: the back of it, from our end, driving:
+--------------------------------------------------------------------------------------------+
|               the DIVIDER at the far end: smoked glass; it slides down (two heads          |
|               with earpieces, and two pairs of dark shades in the mirror)                  |
| THE WINDOWS, left:          the CAR PHONE (a curly cord) and   THE WINDOWS, right:         |
| the desert going by         the ASHTRAY (jelly beans), under   the desert going by         |
|                             the divider                                                    |
| THE LONG SEAT, along the                                       THE FACING SEAT, along the  |
| left: GRANDPA JOE at its    THE CARPET: RANGER                 right: the PAPER BAG, the   |
| far end, in his ROPES (four                                    JUICE BOX, the CLIPBOARD;   |
| strands and a bow) and the                                     THE LITTLE FRIDGE in its    |
| SEATBELT                                                       base                        |
|                                                                                            |
| our own seat, along the bottom                                                             |
|  Here: Grandpa Joe, Ranger                                                                 |
+--------------------------------------------------------------------------------------------+
```

The back of a gray limousine, driving, seen from our end. The desert goes by in the windows on
both sides (a strip of painting, scrolling: outward on each side, as it does from a car going
forward), and the divider at the far end slides down and up. Grandpa Joe is belted to the long seat
and never leaves it; Ranger has the carpet between the seats.

<!-- DRIVE-16M -->
**The windows (round sixteen).** The strip of painting is gone: it showed the same picture on both
sides, moving apart like a mirror. Now the world outside is drawn as it is seen from the moving car,
from the scene's own camera, and each side is its own country (DESIGN.md, section 2, "The world
going by a car's side windows"). Everything comes out of the far end of the windows small and slow
and sweeps out past the near edge large and fast: the far ranges hardly move, the middle distance
drifts, the ground and the posts rush by. On the left, the far edge of the oncoming lane (its white
line rushing by under the glass), the open desert, the long ranges across the valley and a ranch in
the middle distance, white reflector posts, a mile marker, the backs of signs; on the right, a wire
fence along the road, the telephone line far out with its wires, low hills, an OPEN RANGE sign now
and then and one NEXT SERVICES sign. When the limousine slows at the gate, the desert slows with it
to a stop, as before. No puzzle, beat or line changed.

## Cut-scenes and puzzles

```
Cut-Scene: Where the map stops        (opens the act)
```
A dirt lot. Mom: "Thirty-seven miles past Last Gas. This is where the map stops." Big
Sister: "Fun fact: Nevada became a state on the thirty-first of October, 1864.
Halloween." Her mother caps it: "Reformation Day, darling. A matter of record: Martin
Luther's ninety-five theses, 1517." Little Sister: "It's ALL dirt. Who ordered this much
dirt? ...Okay. I'm ready. Where do I start looking for Daddy?" Mom: "Somebody here saw
something. We'll ask nicely. Stay where I can see you, girls." And, looking across the lot
(round twelve): "And there's a gentleman out front with a banjo, and I believe that's a
raccoon. ...We'll ask very nicely."

```
Puzzle #5: Ask Nicely        (Nevada · Lead: Mom · the rocking chair)            a talk (joeTree)
Needs:        nothing
Setup:        One witness: an old man in a rocking chair who has watched this road for forty years and tells
              everybody he did not see nothing. Men in gray suits have already been asking. His raccoon sits beside
              him. Talking to him is a talk (`joeTree` in js/content/talk/nevada.js), and each of the three has her
              own.
The talk:     Mom has four ways in, and each is a choice, not a wrong lead:
                "Good morning. Forgive us for troubling you."  -> "Well, good MORNIN'. Ma'am. Nobody's said good
                    mornin' to me out here in forty years." ("Nobody at all?" "They say 'Is this the road to
                    Vegas.' It ain't." "I promise never to say it." "Then we'll get along, ma'am." "May I buy a few
                    minutes of your time?" "Time's free, ma'am. Lemonade's a dollar. Stories are extra.")
                "May I buy three lemonades?"  -> "Dollar each, ma'am. Jolene squeezes 'em. I pour." He gets up,
                    pours three at the stand beside his chair, and sits back down. Little Sister: "It's got PULP. I
                    LIKE pulp. Pulp is lemonade with CHUNKS." (And he still will not tell her anything: she has not
                    said good morning. "I have quite forgotten my manners. Good morning." puts that right.)
                "What a handsome raccoon."  -> "Ranger. Say thank you to the lady." "..." "He says you're welcome.
                    He's shy with strangers and bold with their sandwiches." (The raccoon is met before he is
                    needed: "And what does he eat?" "Whatever ain't his, ma'am. But he don't eat shiny. Shiny, he
                    keeps.")
                "Is this, by any chance, the road to Las Vegas?"  -> "...No, ma'am." "This ain't the road to
                    Vegas. There ain't no road to Vegas from here. There's a road to NOTHIN', and you're on it."
                    ("I beg your pardon. I was testing you." "Passed, did I." Or "...Is it, though?" "JOLENE! We
                    got another one!" From inside: "Charge her DOUBLE, Joe!" Big Sister: "You asked twice, Mother.
                    The surcharge is just." The lemonade is two dollars for the rest of the act: "Two dollars each,
                    ma'am. Vegas prices." Asked again: "Still ain't, ma'am. Ain't been since the last time you
                    asked.")
              Then the asking. "Did you see a car yesterday, at about a quarter to six?" He answers it only for
              someone who has said good morning (or admired his raccoon); anyone else gets "Didn't see nothing.
              Been not seeing nothing out here for forty years." "The men in the gray suits. Who are they?" "Folks
              come asking about yesterday. Men in gray suits, mostly. I tell 'em I didn't see nothing." "One of
              'em's still out there. Been standin' at that notice since five this mornin'. Ain't had his
              breakfast." (The cheeseburger starts here: "No breakfast? The poor man." "He come in at five wantin'
              a cheeseburger. We ain't sold a cheeseburger here since 1979.") "Why does your sign say GAS, crossed
              out?" "Pump quit in '79. Sign didn't." (Again: "Still quit, ma'am." Again: "Ma'am, that pump is not
              comin' back.") And the way out is a line, a different one each time: "We must not keep you." "Ma'am,
              nobody's kept me since Jolene. You're welcome to try."
Wrong tries:  Little Sister asks          -> her talk is her own: "Mister! Did you see my daddy? He's THIS tall,
                                             he has a scratchy beard, and he's EARLY." "Lemonade's a dollar,
                                             little miss. Stories are extra." "I don't HAVE a dollar. I have a
                                             loose tooth. But it's not for sale. It's waiting for Daddy." And,
                                             new: "Are you MY grandpa?" "I'm everybody's, little miss. Says so on
                                             the sign." "...I have one of those already. But he lives far away."
                                             "So you can be my SPARE one. Grandpa Joe the Rock Wizard. That's your
                                             WHOLE name now." "I been called a lot of things, little miss. That's
                                             the best one yet."
              Big Sister asks             -> she cross-examines him, and it is a choice: "Sir. Did you observe a
                                             red station wagon yesterday at approximately 5:47 p.m.?" "Didn't see
                                             nothing. Been not seeing nothing out here for forty years." "That is
                                             a double negative. Technically, you saw something." "Technically,
                                             I'm closed."
              Mom: "A sensible teal sedan."         -> "No, ma'am. Nothing sensible came down this road yesterday."
              Mom: "A gray car with dark windows."   -> "That's what the gray suits drive. Try again."
Solution:     Mom says good morning (or admires Ranger), and asks about the car. He will talk to family, so he
              tests her: "Depends who's asking. You kin to whoever was in that car?" "My husband and my son." "Then
              tell me what they were driving. The gray suits couldn't." "A red station wagon with wood on the
              sides and far too much luggage on the roof." "That's the one. Red wagon, wood trim, cooler on the
              roof. Driver waved at me. Folks don't wave no more." "Sun was low. Hit the chrome on that wagon and
              threw a flash up ahead, like a signal mirror." "Right where it landed, the sky opened up like a tin
              can. The road sign changed its mind. And that wagon drove straight in." "Hour later the gray suits
              came and put up a fence. 'Radiation,' they say. Third piece of desert they've shut this year." He
              looks up the road toward the glass, a hand to his hat. Then, asked whether anything else has been
              strange this week, first the hens: "Been a strange week. Jolene's hens quit layin' the day the sky
              opened. Stand out back all day now, facin' that fence." "Jolene says it's the sky. I say it's my
              banjo." Little Sister: "That's EVIDENCE. Chickens KNOW." And, asked again, the coin: "One more thing.
              Somethin' come down out of a clear sky about an hour after, and hit my hat. Rang like a bell.
              Silver." "I'd give it to you, ma'am. Only it ain't mine no more. Ranger had it before it quit
              ringin'." He touches his hat (the dent), and Ranger looks at Mom. "A silver coin. In the keeping of a
              very serious raccoon." "He don't steal. He trades. You just weren't there for your half."
Gives:        The witness's account, and where the coin is (`nevada.witness`: it comes true when he tells of the
              coin). His hint for #10, asked "And what would he take in trade?": "Ranger's partial to shiny. And he
              don't like grabbers."
Plants/pays:  Pays off the intro (the sign that changed its mind) and the look of the wagon. The coin is
              the one the Son tossed through the coin-sized door in Rome ("Why is the sky DOWN?"). Plants the
              flash of low sun, which he tells without knowing it is the part that matters: it pays off in #9,
              and again in #12. (Ask him again, as Mom: "The flash of light, if you would. From the top." "Low
              sun on bright chrome, ma'am. One flash, up ahead. And where it fell, the sky came open. Never seen
              the like.") Plants the Geiger counter that never clicks. Pays off "Chickens KNOW." (Act Three):
              the hens are Jolene's now, and they are out back, facing the fence: #11. Plants the cheeseburger.
Notes:        The tree is `joeTree`, from the sample in the story document (section 9), with the design's three
              changes (good morning; the hens are Jolene's; the coin is Ranger's). Where the sample and the act's
              own lines said the same thing, the act's words were kept. His kept lines are word for word, with no
              accent added; the rest of his lines are lightly Southern. Each of the girls has her own talk with him.
              After the coin, Little Sister's lemonade is on the house ("Your ma's good people. Lemonade's on the
              house, little miss." "On the house? WHERE'S the house? ...Thank you, Mister Rock Wizard. You're a
              GOOD wizard."). She can ask him to play ("Can you play your banjo? PLEASE? I'm a GOOD listener."
              "This here's the Last Stop Rag, little miss. I wrote it. Nobody's ever asked to hear it twice."),
              and he plays a few bars in his rocker, and the chrome of the banjo flashes in the low sun: "It did a
              FLASH! Your banjo did a FLASH in the sun! Did everybody SEE?" "Does that when the sun's low. Jolene
              says it's showin' off." (Asked twice: "...Twice? Little miss, in forty years you're the first.")
              Big Sister asks about radiation ("Sir. They say radiation. Do you own anything that measures it?"
              "My daddy's Geiger counter. Clicked fine for him in fifty-seven. Hasn't clicked once this year."
              "Then somebody is lying, and it isn't the Geiger counter. Interesting.") and about Ranger ("The
              raccoon. Is he yours, or are you his?" "Bit of both, miss. Mostly I'm his."). Hints: Mom, "The
              gentleman in the rocking chair has had a front-row seat on this road for forty years. Nobody has
              asked him nicely."; Big Sister, "The old man is a witness, and he doesn't care for my questions. Mom
              could get a statue to talk."; Little Sister, "The Rock Wizard won't tell ME. He wants a dollar.
              Mommy has dollars AND manners. Mommy should ask him."
```

```
Puzzle #10: Ranger's Trade        (Nevada · Lead: Big Sister · Ranger, by the rocking chair; the mirror shades are in the store)
Needs:        #5
Setup:        The coin is in Ranger's basket under the store counter, and Ranger sits beside Grandpa Joe's chair.
              A raccoon trades: one shiny for one shinier, both hands out, and he looks it over first. Talking to
              him is a talk (`rangerTree`): he says "...", and Grandpa Joe says what he means.
Wrong tries:  Little Sister at Ranger, empty-handed -> "Ranger? About the shiny money."
                                           "Give me the coin, please. It's EVIDENCE." "..." Ranger turns round and
                                           shows her his tail. Grandpa Joe: "That's a no, little miss."
              Mom at Ranger              -> "Ranger, I believe you have something of ours." "..." "I have
                                           negotiated with a seven-year-old, a thirteen-year-old and a man who
                                           keeps ketchup in a vault. I draw the line at a raccoon." Grandpa Joe:
                                           "He'd take that as a compliment, ma'am." (The same if she holds the
                                           mirror shades out to him.)
              The take-a-penny dish, in the store -> Little Sister takes a penny. "It SAYS take a penny." Big
                                           Sister: "It says take A penny." "I'm taking a penny A LOT of times."
                                           Three more. "One, two, three, FOUR. Four pennies. I'm RICH." A penny
                                           held out to Ranger: he takes it, sniffs it and hands it back. Grandpa
                                           Joe: "He don't want copper, little miss. He wants to see himself in
                                           it." (Put in his basket in the store, Jolene: "He don't want copper,
                                           sugar. He wants to see himself in it.")
              Little Sister with the mirror shades -> "Look, Ranger! SHINY! Do you want them? You can have them!"
                                           She holds them out, and snatches them back when he reaches: "I'm not a
                                           GRABBER. I'm a HOLDER." Ranger, to the tail again. Grandpa Joe: "He's
                                           particular about manners, little miss."
              Ranger's basket, under the counter -> Jolene: "Nobody goes in that basket but Ranger. Not me, not Joe,
                                           not the government."
              The spinner rack, as one of the girls -> Big Sister: "I have no money. I have a great deal of
                                           knowledge, which is not legal tender." Little Sister: "Mommy, can we buy
                                           the SHINY ones? Mommy BUYS things. That's how buying WORKS."
Solution:     Mom buys the last pair of mirror shades off the spinner rack: "We buy, girls. We do not borrow." She
              takes them off the hook and pays at the register. Jolene: "Three dollars and ninety-nine
              cents, sugar. Last pair. They been waitin' on you." The register rings, for her: "There. She rang.
              She don't ring for just anybody." Mom hands them to Big Sister, and Big Sister trades, in Ranger's
              talk ("Ranger. I would like to propose a trade.") or by holding the shades out to him. She has the
              fact: "Fun fact: a raccoon's most important sense is touch, and water is thought to make his front
              paws feel even more." "So: both hands out, flat, and hold very still. Let him read it." She holds
              them out flat on both hands and keeps still. Ranger takes them, turns them over in his paws, looks at
              himself in the lenses, scampers into the store for his half of the bargain and back, and puts the
              coin in her hand. "...Thank you. That was very correct of you." He puts the mirror shades on, and
              wears them for the rest of the game.
Gives:        The coin, to Big Sister (`nevada.traded`), and she reads it there and then (#6).
Plants/pays:  Pays off "Chickens KNOW" the other way about: a raccoon knows a grabber. Plants Ranger's
              manners for Act Five: he trades, he feels with his paws, and he is a very good judge of ropes.
              The shades on Ranger are the running sight gag of the limousine.
Notes:        Little Sister cannot do this one, and it is the first time in the game that she minds: "I would
              have been GOOD at that. If he'd let me." Big Sister: "You would have been fast at it." The trade is
              offered only once Grandpa Joe has said that the coin is Ranger's (#5). In Ranger's talk Little
              Sister holds long conversations in which she does both parts ("What's your favorite color?" "..."
              "SHINY? Shiny's not a COLOR, Ranger. ...He says it is NOW."), Mom says good morning ("He says good
              mornin', ma'am. Nobody says it to him neither."), and Big Sister tells him his Latin name ("Fun fact:
              your Latin name is Procyon lotor. 'Lotor' means 'washer.'" "..." "He says he knows, miss. He just
              don't like to brag."). Hints: Mom, "Ranger trades shiny for shinier, and there's something shiny
              for sale in that store. We're a family that buys."; Big Sister, "A raccoon feels with his front paws.
              Something shinier than a coin, held out flat on both hands, and kept very still."; Little Sister, "He
              likes SHINY. The store has SHINY. I saw it SPIN."
```

```
Puzzle #6: Hand Over The Coin        (Nevada · Lead: Big Sister)
Needs:        #10
Setup:        Ranger puts the coin in Big Sister's hand, and she is the one who knows what it is.
Wrong tries:  Give it to Little Sister    -> "I get to HOLD it? Finally! Hi, grumpy man. You're with ME now.
                                             I'm holding you with BOTH hands." (She can pass it on.)
              Give it to Mom              -> "Thank you, darling. It goes in my handbag, with everything else
                                             that matters."
              Show it to Grandpa Joe      -> "Don't show it to Ranger. He'll want it back." (round twelve: he
                                             did not give it to them, so Mom's old line went)
              Show it to the man in gray  -> "I can neither confirm nor deny that that is a coin."
                                             "If it were a coin, I would have to file a report. So it is not a coin."
Solution:     Big Sister reads it as soon as Ranger puts it in her hand (round twelve: #6 falls together with
              #10). "Mother. This is a Roman denarius. And that is Julius Caesar." "Fun fact: in 44 B.C., coins
              were struck in Rome with Caesar's own portrait. While he was alive." Little Sister knows it at once:
              "It's the Caesar money from Sunday school!" Big Sister has the fact: "The 'penny' they brought to
              Jesus was a denarius, like this one. Most likely with a later Caesar on it: Tiberius." And Mom has
              the verse: "'Render therefore unto Caesar the things which are Caesar's; and unto God the things
              that are God's.'" Then Big Sister goes back to the coin: "And it isn't two thousand
              years old. Look at the edges. It is NEW. It has hardly been in a pocket." Mom: "A new coin, from 44
              B.C., that fell out of the sky. In Nevada."
Gives:        Half the answer: a new coin from 44 B.C. (`nevada.coinRead`).
Plants/pays:  As before: pays off the Son's coin toss in Act Two; plants that the coin is new, which is to say
              that it shines (#9). Once the coin has been read, a word between Mom and Big Sister: "A matter of
              record: Caesar put his own face on his money. Ours says 'In God We Trust.'" "Fun fact: first in
              1864, on the two-cent piece. The year Nevada became a state. That half is mine."
Notes:        Kept as it was, with the coin now coming from Ranger (#10) and not from the old man. The design let
              her hand it to her mother first, unread; the scene has her read it on the spot, since a carried
              thing's look cannot call the scene. So two of Mom's lines, for a coin nobody has read yet ("I have a
              coin that fell out of the sky, darling. I'd like your professional opinion." "Then hand it over, Mother. I can't
              footnote what I can't hold."), and this beat's three hints are written and never heard. (Mom's own
              look at the coin, "A silver coin with a stern gentleman on it. It looks old and it looks new. Your
              sister will know which.", is heard only once it has been read.)
```

```
Puzzle #7: Ask Two Hundred Questions        (Nevada · Lead: Little Sister · the fence)
Needs:        nothing
Setup:        There is a notice on the fence. A man in a gray suit is standing exactly in front of it.
Wrong tries:  Read the notice             -> each of them can see AREA CLOSED above his shoulders and none
                                             of the small print, and says so. Big Sister: "I can read
                                             'AREA CLOSED'. The small print is behind his jacket, which I
                                             assume is the point."
              Mom asks him to move        -> "Good morning. May we read the notice behind you?" "There is no
                                             notice, ma'am." "I can see all four corners of it." "I can neither
                                             confirm nor deny a corner."
              Mom asks a second time      -> courtesy, with the rule book named. "A matter of record:
                                             by the time he was sixteen, General Washington had copied
                                             out 110 rules of civility." "I can neither confirm nor
                                             deny General Washington." "Then you have not read one of
                                             them. Good morning."
              Big Sister asks on what authority -> "I can neither confirm nor deny that it is an area."
                                             "It has a fence." "I can neither confirm nor deny the fence."
Solution:     Play as Little Sister and talk to him (looked at, he is named already: "I'm naming him
              Mister Gray."). She counts her questions on her fingers: "Hi, Mister Gray! I have some
              questions. Number ONE: why is your tie gray?" "Move along, little girl." "That's not an
              ANSWER. Number two: is your car gray? Three: is your DOG gray? Four: do you HAVE a dog?"
              "I can neither confirm nor deny a dog." "Five: what's his NAME? Why are you standing THERE?
              Is it your turn? Do you get a snack? That's EIGHT fingers. I have TOES too." (Round
              twelve: he answers the snack, once, to himself: "...I have not had a snack since 0500.")
              Into his earpiece: "...Sir? It's me. I have a situation. No, sir. She is about seven. She
              has a list." He retreats along the fence, and she goes with him: "Who are you talking to?
              Is it your mommy? Tell her you're not DONE. ...Hi, Mister Gray's mommy!" (Round twelve: the
              earpiece answers, small and far, and only the player hears it: "Jed, is that the child
              again?" Nobody repeats it.) Big Sister: "'It was,' she noted, 'the finest interrogation
              she had ever witnessed.'"
Gives:        A clear view of the notice (`nevada.distracted`). He stays busy for the rest of the act ("You
              stay RIGHT there. Next question. Why is the sky? Not why is it BLUE. Why IS it?" "...Sir?
              Requesting a transfer. To a quieter desert.").
Plants/pays:  Pays off "ask a LOT of times". Looking at the fence, she says: "I could fit under that.
              I fit under EVERYTHING. ...I'm just SAYING." That is for the next act. Mom's second try pays off Act Three, on the
              landing ("as a schoolboy, George Washington copied out 110 Rules of Civility"). Plants Jed's
              lunch ("...I have not had a snack since 0500.") and his name.
Notes:        Courtesy cannot move him, and neither can logic. The notice itself says "No questions."
```

```
Puzzle #8: Read The Notice        (Nevada · Lead: Big Sister · the fence)
Needs:        #7
Setup:        The notice can be read now: AREA CLOSED. BY ORDER. ELEVATED RADIATION LEVELS.
              SECTORS 44 AND 1921 SEALED UNTIL FURTHER NOTICE.
Wrong tries:  Mom reads it                -> she reads it out. "Sectors. Somebody has numbered the
                                             desert. Your sister should see this."
              Little Sister reads it      -> "It says... A, R, E, A. AREA! I can READ that. And a yellow
                                             spinny flower. 'Radiator levels.' That's bad, right?"
Solution:     Big Sister reads it. "'Elevated radiation levels.' In Nevada, people will believe that. Fun
              fact: atomic bombs were tested out here from 1951 until 1992." "Which makes it a very good
              excuse. But look at the sectors. Forty-four. Nineteen twenty-one." "Nobody numbers sectors like
              that. Those aren't places, Mother. I think those are years."
Gives:        The other half of the answer (`nevada.notice`).
Plants/pays:  44 and 1921 are the years the Son and Dad are in. Whoever put up the fence knows that.
              Both are on Big Sister's timeline at home (Act Three): she says so in "Some when". The
              office's own map, in Act Five, has a third sector.
Notes:        Whichever of #6 and #8 comes second, she joins them up on the spot: "Sector 44. A new coin
              from 44 B.C. It is the same forty-four. The holes don't go to places. They go to YEARS."
```

```
Puzzle #11: Jolene's Girls        (Nevada · Lead: Little Sister · the store, and out the back door)       a talk (hensTree)
Needs:        nothing (the store is open from the first line)
Setup:        Grandma Jolene's hens have quit laying, and they stand out back in a row, facing the fence: through
              the open back door, five small hens with their backs to us. Asked for the sun shade in her window,
              she will not part with it: "Then I'd have an empty window, sugar. A store with an empty window is a
              shed." Again: "Not the window, sugar. Anything but the window." And again: "Sugar, you could ask
              me with a cherry on top. You do somethin' about my girls, and we'll see."
Wrong tries:  Mom asks about the hens      -> in Jolene's talk: "And how are your hens, Mrs. Jolene?" "Oh, you're
                                              kind to ask. They won't talk to me. They won't talk to Joe. They're
                                              not talking to anybody. They just LOOK." "At what?" "The fence,
                                              sugar. Day and night. Like it owes them money."
              Big Sister on the hens       -> "Fun fact: a hen lays less when she is frightened." Jolene: "They
                                              ain't frightened. I know frightened. Frightened goes UNDER the
                                              porch." Big Sister, who cannot stand it: "That is... actually a
                                              fair point."
              Mom or Big Sister at the back door -> "I'm not going to stand in a hen yard, darling. I've stood
                                              in worse, and I have standards." / "I will observe from the
                                              doorway. That is what a doorway is for."
              Little Sister on the step, first -> what she tries first is the player's choice, each once: "Flock!
                                              ATTENTION!" "...Nothing. They're not MY flock. You can't order
                                              somebody else's flock. That's RUDE."; "Hi, chickens! I'm new here.
                                              I'm VERY good with chickens." "...They didn't even LOOK. They're busy
                                              looking at something ELSE."; "Bawk? Bawk BAWK?" "That's hello, in
                                              chicken. ...They can tell I have an ACCENT."
Solution:     Play as Little Sister and go out of the back door onto the step (or, in Jolene's talk: "I speak
              chicken. I'll go out and ASK them what's wrong." "You go on, sugar. Back door's open. They ain't
              told me a thing all week."). The first time, the other two come and watch from the doorway, and
              Jolene calls the names after her: "Darlene, Charlene, Marlene, Arlene and Doreen. Named for my
              sisters. The hens are nicer." Then the hens' talk. "Okay. I'll stand in the row with you. And look
              where YOU look." She faces the fence with them. "The fence. ...The Hummy Place." "...Oh. They're not
              scared. And they're not waiting. They're GUARDING." "Somebody went in there, and they're keeping an
              eye on it till he comes back." "That's what General Feathers is doing for Daddy. Chickens KNOW when
              somebody needs minding." (She may salute them first: "I'll SALUTE them first. That's what you do
              for guards." "...They didn't salute back. They're ON DUTY. That's allowed.") "I'll TELL them. One
              at a time, by name. That's polite." In her order: "Darlene. It's okay. My family's going IN there.
              We're going to get them. You can stand down." Darlene turns round to look at her, and sits; Jolene
              comes out from behind the counter to the doorway to see. "Charlene. You too. Stand DOWN. That's an
              order. ...A NICE order." Charlene sits. "Marlene, Arlene, Doreen: you can keep guarding if you WANT.
              Somebody should. Thank you for minding them." Darlene stands up, and there is an egg in the dust.
              "...An EGG! Darlene did an EGG! Right THERE! In the DIRT!" Jolene, in the doorway: "Twenty-two years
              I've kept hens. Nobody ever TOLD them anything." "Anything in this store is yours, sugar. The window
              too. Not the pickled eggs. Those are Joe's." "And that egg's yours to carry. For luck. Darlene'd want
              you to have it." Little Sister hops down into the yard for it, and back onto the step: "It's WARM!
              I'll keep it in my FRONT pocket, with my hand on it. Like a NEST."
Gives:        Jolene's friendship, which is the run of the store, the window too (`nevada.jolene`). And one warm
              egg, which Little Sister will not hand to anybody: "It's WARM. It's MINE to keep warm." (Handed to
              one of the others, it comes straight back.) Darlene and Charlene sit from now on; the other three
              keep guarding, and peck now and then. Back on the step: "Hi again, girls. Still guarding? GOOD. You
              keep GUARDING."
Plants/pays:  Pays off "Chickens KNOW" (Act Three, Little Sister's room), the RESERVED pillow and General
              Feathers in Dad's suitcase, and the hens facing the fence (#5). Plants the hens turning round,
              all five, to watch the limousine go (the cut-scene), and the egg (the one thing in her pocket that
              has to be kept warm, wherever they land).
Notes:        This is the author's "bonds with Little Sister over chickens", written so that the bond is the
              puzzle: the hens will not be ordered, and the one person at the Last Stop who knows that is seven.
              Jolene and Little Sister talk like two colleagues (`joleneTree`): "Can I see your chickens? I'm VERY
              good with chickens. I have a whole FLOCK." "Do you now! What do you feed yours?" "Everything.
              They're not fussy. Admiral Doodle ate a crayon." "Which color?" "Blue." "...They do like a blue."
              Jolene's talk has her facts too, one a visit, four in all, each wrong beyond argument, each put
              right by Big Sister: a hen has teeth; a raccoon has a pocket; a good hen lays one on the hour; the
              rooster lays on Tuesdays (the first is the one she calls a fun fact: "It's fun and I said it, so
              it's a fun fact."). Hints: Mom, "Mrs. Jolene would do anything for anyone who did something for
              those hens."; Big Sister, "The hens are the key to the store, and I am not the key to the hens.";
              Little Sister, "I speak chicken. I'll go and ASK them."
```

```
Puzzle #9: Flash The Coin Where The Tracks Stop        (Nevada · Lead: whoever holds the coin · the patch of glass)
Needs:        #6 and #8
Setup:        Tire tracks run out from under the fence and stop at a patch of sand that has turned to
              glass. There is nothing else to see. Little Sister, looking: "The ground's all SHINY. And it
              hums, like a bee in a jar. But there's no bee. And no jar. It's the Hummy Place."
Wrong tries:  Go to the tracks before both halves: Mom -> "Not yet, darlings. I'd like to understand it
              before anybody stands on it." Big Sister -> "I have a theory. A theory is not a fact until I can
              footnote it." Little Sister -> "I'll jump on it first. I'm the lightest, so it's SAFEST. ...Mommy's
              doing the eyebrow. That's a no."
              The coin at the tracks before both halves -> the same.
              Little Sister's flashlight where the tracks stop (at any time, whoever is holding it)
              -> Little Sister: "CLICK. It's ON! ...Where's my spot? I can't even SEE my spot. The
              sun's got a WAY bigger flashlight." Nothing opens. Light is the right idea, and this
              is too little of it. (Tried anywhere else, and the other four things from the house
              tried anywhere at all: the game's stock replies.)
              The sun shade from the store's window, at the glass, after both halves -> too soon (#12): "One thing
              at a time, darlings. The coin came out of that sky. Let us begin with the coin." / "Not the window.
              Not yet. An experiment starts small: the coin first." / "The WINDOW is for later. First the shiny
              MONEY. I just KNOW it."
              Go to the tracks after both halves, with nothing in hand -> she listens, and remembers
              the old man. Mom: "It hums, darlings. Very quietly, and a little flat. Like your father
              when he's lost and won't say so." "The gentleman said a flash of low sun fell just
              here. I wonder what we have that flashes." Big Sister: "It hums. Right here, over the glass,
              where there is nothing at all to hum." "A flash of low sun fell here, and the sky opened. That
              is his whole story. So: we need a flash." Little Sister: "It HUMS! Right THERE! There's nothing
              there and it HUMS! ...Hello? Daddy? Are you in there?" "The Rock Wizard said the car went FLASH
              and the sky went OPEN. So we need a flash. I'm READY."
Solution:     Use the coin where the tracks stop, as whichever of them is holding it. Mom: "Places,
              girls." The one with the coin goes to the corner of the glass, and the other two stand
              back. Big Sister: "The tracks don't turn. They don't skid. They just stop." Then, first
              things first: Mom bows her head, and the girls with her. Nobody has to be told. "Father,
              You brought us this far. We don't understand what comes next. You do. Keep us, and
              keep them. In Jesus' name." Little Sister: "And thank You for the lemonade. And tell Daddy
              we're COMING, so he doesn't have to be brave by himself. Amen." Heads up, and the coin goes
              up into the low sun. Each has her own
              line for it. Mom (and only when it is she who holds the coin, a line before it: "Dr.
              Franklin said the sun carved on General Washington's chair was 'a rising and not a
              setting Sun.' So is this one."): "Stand back a little, girls. I'm about to do
              something your father would think of." Big Sister: "A low sun. A new coin. And an old
              man's story. This is called an experiment." Little Sister: "My turn! I'm gonna do a
              FLASH, like the car did! Everybody stand BACK. And WATCH." One flash. The light stays where it fell,
              over the glass, and a door opens there, exactly the size of the coin.
Gives:        A door in time the size of a coin (`nevada.doorOpen`), and the scene "Some when". (Round
              twelve: no longer the act's gate, and no longer the end of the demo. #13 is the gate.)
Teaches:      Their half of the rule of the doors: light opens them. (A coin's worth of light, a coin's
              worth of door: they have not been told that yet, and Mom's last line knows it anyway.)
Hints:        Mom: "A flash of low sun opened the sky where the tracks stop. We have a low sun, and a
              very new coin." Big Sister: "A flash of sun opened it once. The sun is low again, and the
              coin is new enough to flash. Where the tracks stop." Little Sister: "The shiny money can
              do a FLASH, like the car did! At the Hummy Place, where the car tracks stop! I'm READY."
Plants/pays:  Pays off the old man's flash (#5), the newness of the coin (#6), and the Son's "little
              light, little door" in Rome, which nobody here has heard.
Notes:        Any of the three can do it, and each has her own line: the coin can be handed round
              first. Until this moment there is nothing of the door on the screen. The light is drawn
              live: the flash of the coin (`#spark`), a short beam (`#ray`) and the spot where it lands
              (`#glint`), all out of sight until the coin goes up. The door itself is the paint bending
              (the engine's `portal`, the scene's effect `door`, the size of a coin), shut until the light
              has fallen on it. They pray, and then they do the experiment: it is the light that opens the
              door, here as everywhere, and nothing on the screen says otherwise. While the prayer is said all
              three stand in the game's praying pose (`actor.pray`: head bowed, hands folded, each in her own
              way), and it is let go before anyone reaches or walks. Round twelve: the two who are not holding
              the coin watch from a row further back than before, because Grandpa Joe sits behind them now.
```

```
Cut-Scene: Some when        (the middle of the act now; round twelve)
```
Little Sister is at the door before anybody can say no: it is at the height of her eye.
"A HOLE! In the AIR! And it's littler than ME! ...I bet I could still FIT." Big Sister
narrates it: "'The air,' she noted, 'now had a hole in it. A hole exactly the size of the
coin.'" Little Sister, with her eye to it, hears them first, and counts them: "SHH!
Everybody SHH! ...CHICKENS. Three! No, FOUR! I can hear CHICKENS in there!" And then:
"It's a DIFFERENT sunny in there! And it smells
like SAUSAGES!" Mom: "Chickens. She is quite right. And sausages, and bread, and
woodsmoke." Big Sister: "It is morning in there, too. I do not think it is THIS
morning." "Then which morning, darling?" She gives both, and at the first of them Little
Sister, with her eye still at the door, has a question: "Sector 44: forty-four B.C. The
year Julius Caesar was killed, on the Ides of March." "Wait! What's B.C.? Somebody tell
me QUICK." Mom: "Before
Christ, sweetheart. Before Jesus was born." "Sector 1921: nineteen twenty-one B.C. It is
on my timeline: the year Abram went down into Egypt." Her mother knows the chapter:
"Abram going down into Egypt. I've read that my whole life. I never once thought of it as
an ordinary morning." And Big Sister sees a pattern she cannot explain: "The Ides of March.
Abram in Egypt. The holes open on years that MATTER. ...I don't know why." "They didn't
crash, Mother. They didn't go anywhere. They went some WHEN." Little Sister, turning
round to them: "I TOLD you! Daddy's not lost! Daddy's EARLY!" Big Sister: "...Nearly four
thousand years early. She was right. I need to sit down." Mom: "'My times are in thy
hand'... All of them, girls. Even that one." "Then we know
where they are. And we have a door. It is only a little small." "Girls. We are going to
go and bring them home."

"Daddy's EARLY" is the top of the scene, and is word for word the line the author asked
to keep. It is still Little Sister's last word. Four lines follow it: Big Sister's, the
psalm, and the last two exactly as they were. ("Then we know where they are" now follows
the psalm, and means two things. Not a word of it was changed.)

*"Wait! What's B.C.? Somebody tell me QUICK."* is what makes EARLY land: she is told
"before", and a few lines later she has done the sum her own way. It is asked and answered
at the Roman year and nowhere else.

*The second year* is the Bible's own count, as Archbishop Ussher counted it (see "How the
game counts the years" in [CHARACTERS.md](CHARACTERS.md)): 1921 B.C., the year Abram went
down into Egypt (Genesis 12:10), and it is on Big Sister's timeline at home. She tells it
in her own words; her mother names the chapter and does not quote it. "Nearly four
thousand years early" is the sum: from 1921 B.C. to A.D. 2026 is 3,946 years (there is no
year 0). Nobody here speaks of the pyramid.

*The pattern.* Both years are years when something happened: the doors open on years
that matter. Big Sister notices it, once, and does not know why. It is a plant, and
nothing pays it off yet.

*What comes through the door, and why it is so little.* Chickens; a different sunlight;
the smell of sausage, bread and woodsmoke. That is a March morning in Rome in 44 B.C. as
Act Two has it (the soothsayer's sacred chickens on the temple steps, facing the temple
doors, and the snack bar's bread and sausage), and it is all they get. Little Sister hears
the chickens before anybody smells a sausage: chickens are the first thing she would
notice anywhere, and she is always right about them. They do not see the Son, hear him, or
learn which of the two years is in there: Big Sister names both and chooses neither. (Round
twelve: they do hear him later, when one of them speaks into the same door: the letterbox,
below.) The player, who has been to Rome, knows more than the family does.

*Plants:* the way through is here, it is too small, and somebody official is standing
a few steps from it with his back turned, reporting a seven-year-old to his superiors.

<!-- NEVADA-12W -->
*Round twelve: the scene no longer ends the act.* Instead of the title, one more beat, and
play. Little Sister turns back to the hole: "I STILL bet I could fit. ...Just my HEAD. I'm only
going to try my HEAD." She goes up under it and leans in, to the ears. From inside, muffled:
"It's WARM in here. ...Mommy, there's a chicken LOOKING at me." Mom comes and lifts her out by
the collar, as one lifts a cat out of a drawer: "Not head first, sweetheart. Not into any
century." Big Sister, who has not stopped looking at the hole: "It is exactly the size of the
coin. The coin was exactly the size of the flash." "...Mother. I think I know what the old man's
story was about." And she says the rule, in three lines: "A small flash, a small door." "A car's
worth of flash, a car's worth of door." "We don't need a bigger sun. We need a bigger SHINE."
Mom: "Something that shines like a station wagon." And Little Sister, if she has seen the banjo
flash (she asked him to play): "Grandpa Joe's BANJO shines! I SAW it! It did a FLASH when he
played!" Then play goes on, with the little door open over the glass.

<!-- LETTER-17: the night Mom hears her son (round seventeen) -->

```
The letterbox: Is That YOU?        (Nevada · any of them · the little door)       a talk through the door (letterboxTree)
Needs:        #9
Setup:        On the other side of the coin door is the Son, in Rome, holding his own coin door open with Dad's keys
              in the sun. Through a door the size of a coin, voices carry. From #9 until #12 the little door is a
              thing to click ("Talk into"); his words come through it, top centre, with his portrait. (Round
              seventeen: the night Mom hears her son, rewritten as the author asked on 16 October. She must answer
              as a mother would when she hears her son, and he must explain as best he can until she understands
              that he is in another time.)
The talk:     Whoever speaks into it first hails it. Mom: "Hello? ...Is anybody there? I'm talking to a hole in the
              air, girls. Nobody tell your father." Big Sister: "Hello. This is a test. If anyone can hear this,
              please say so. Clearly." Little Sister: "HELLO! Is anybody IN there? It's ME!" He answers: "Hello?
              HELLO? Is somebody out there? This hole has VOICES in it." At his voice Mom's handbag goes down on the
              gravel (the first time in the game she has put it down without looking), and she is at the door on her
              knees, facing it, while he and his little sister say hello: "...Is that YOU?" "Is that YOU?" "I asked
              FIRST." "I asked EARLIER."
              Then Mom, and every rule of her voice is gone at once: "Baby? Is that you? Are you okay? Are you hurt?
              Where are you? Is Daddy with you?" "Mom! Hi! I'm okay! Don't freak out." "I'm not freaking out. Why
              would I freak out. Where ARE you?" Big Sister, very quietly: "She's freaking out." Little Sister: "I
              know. It's AWESOME."
              He explains, as best he can. Through a door the menus are his words, so the player chooses what he
              tries next, each once, and each try gets the answer a mother would give and moves her a step from
              Italy to 44 B.C.: "I'm in Rome!" "Rome. ...Rome, ITALY? How did you get to Italy? Who took you to
              Italy?"; then "It's not THAT Rome. It's old Rome. Like, OLD old." "Honey, I need you to not be funny
              right now." "I'm NOT being funny! ...For once."; the smell ("It smells like sausages out here. And
              bread. And smoke. And one other thing I'm choosing not to know." Big Sister: "Sausage, bread,
              woodsmoke. What we smelled through our side." Mom: "Whatever the other thing is, don't touch it.");
              the chickens ("They have sacred chickens! In a CAGE!" Little Sister: "I KNEW it! I HEARD them! I heard
              them FIRST!" Mom: "...Chickens."); Caesar ("Caesar's on the money. And he's ALIVE. Everybody keeps
              yelling about him." Mom: "..." Big Sister: "Caesar on the money, and alive. Mother, that's our
              coin."); the togas ("Everybody's wearing bedsheets, and nobody has a car. I asked." "Togas." "Who's
              watching you? Is there a grown-up there? Put a grown-up on." "There's a man counting money. He's up to
              four hundred. I don't think he does phones."); and the temple ("I'm in a temple with giant stripy
              pillars. They keep the money in here. With the god." "Are you allowed in there?" "...Mostly."). Once
              three of the five clues are in (the smell, the chickens, Caesar, the togas, the temple, as before), he
              can tell her: "Mom, it's B.C. I checked. It's before the red mark on Big Sis's timeline." "...Before."
              Big Sister pins it: "A new coin from 44 B.C. Sector 44 on the notice. And everything he's told us
              fits." "Mom. He's in Rome. In 44 B.C." And Mom, slowly: "He's not in Italy. ...He's in Rome. Then."
              She sits back on her heels, and the girls come and stand either side of her. "...Mom? Are you okay?"
              She comes back, up on her knees at the door, to the next thing she can fix: "...Have you eaten?"
              ("Mom. I'm in ROME. That's your question?" "It's always my question. Answer it.") "Bread with cheese
              IN it. Nine out of ten. It needed ketchup." "...Okay. Okay. Then I can think."
              After that, what else he may say, with a mother's real questions in it. "Can you send me something?
              Anything? A snack would be ideal." If the one talking has the lucky penny: "I'm sending you a PENNY.
              For LUCK. Here it comes!" Little Sister goes up to the door and pushes it in, and the door winks.
              "...Nothing came out. Did you SEND it?" "I SENT it. It's taking the LONG way. Pennies are SLOW."
              "...Would a CHICKEN fit?" "No." "Please don't post me a chicken. I've got chickens. They're SACRED."
              (If somebody else is talking: "I've got a PENNY for him! But I post it MYSELF. It's MY penny." If
              nobody has taken a penny yet, Mom: "Nothing small enough to send yet, baby. We'll look.") "I'm holding
              my door open with Dad's keys, in the sun. My arm is SO tired." "Your father's keys. He never lets
              anyone hold his keys, sweetheart. He must be very sure of you." "There's a cat in here. She's asleep
              on the treasure. She's very official." "Are you warm enough? Is your hoodie zipped up?" "Zipped. And
              now the cat's asleep on MY feet. Ten out of ten." "I'm not even tired. It's been morning here for
              AGES." "And tonight? Where are you going to sleep?" "...Operation Tonight is still in the planning
              stage." "Then you find a kind lady with a warm kitchen, and you ask her. Nicely." "Everybody's really
              nice here. Except the door guy. He scores people out of THREE." "Who? Who's being kind to you?"
              "Walnut. He's my best friend now. He's the best at nuts on the whole street." "...You tell Walnut
              thank you. From me." "What's it like over there? Tell me EVERYTHING." "There's a RACCOON. And a
              grandpa with a BANJO. And a lady with a HAT. And a PAY PHONE. On a WALL." "A PAY PHONE? I've got a
              QUARTER for one of those!" "It does not work." "...I'm keeping the quarter anyway." "Is there a dog?
              Please tell me there's a dog." "There's a RACCOON. He's like a dog with a MASK on." "...Ten out of
              ten. I'll allow it."
              The first time, his warning, which ends the talk: "Mom. Wait. I have to tell you something. It's
              important." "Dad went through his door to come and get me. He didn't come out. Don't go through
              yours." A pause. "...I hear you, baby." She does not promise. Big Sister: "She didn't say no." "Stay
              where you are. Keep your door in the sun. We'll find you." Little Sister: "We're COMING. That's what a
              family DOES." "...Okay. Then bring snacks." "I love you. You hear me? I love you." "Love you too.
              ...Don't tell anybody." Big Sister: "Noted." "BYE! I asked FIRST!" "I asked EARLIER!"
              Grandpa Joe heard all of it. Mom gets up off her knees, and from his rocker: "Ma'am." She turns to
              him. "That's a good boy you got." "He is." "I been sittin' out here forty years watchin' the sky not
              do anything. ...You tell me what you need, and I'll hold it." Ranger comes down off the porch at a
              scamper, sits up beside the handbag, picks it up by its strap and holds it up to her: "..." "He says
              you dropped this. He didn't look inside. ...He looked a little." She bends and takes it, and it is on
              her arm again. "...Thank you, Ranger." He goes back to his place by the rocker.
              Spoken into again: "You're BACK! I'm still here. Still holding the keys. Still a little hungry." Then
              the rest of the talk, and goodbye: "I have to go. My arm's about to fall off, and the counting man is
              giving me a look." "Talk later, my love. Keep your door in the sun." "BYE! I asked FIRST!" "I asked
              EARLIER!" (A first talk broken off, in a game saved in the middle of it, picks up after "You're BACK!"
              where it was, with Mom at the door on her knees and her handbag on the gravel.)
Wrong tries:  The little door, looked at -> too small to go through: "Not yet, girls. It's a door for a coin, and there
                                           are three of us." / "It is the size of a coin. I am not." / "I could fit
                                           my HEAD. ...Mommy says not head first."
              The three pennies, or the egg, on it -> Little Sister will not part with them: "No! They're MINE. I
                                           took them FAIR. It SAID." / "It's WARM. It's MINE to keep warm."
              The coin on it              -> "Then we know where they are. And we have a door. It is only a
                                           little small."
Gives:        `nevada.heardSon`: round seventeen, it comes true at the end of the first talk, with his warning and
              her answer (it used to come when he had said what he ate). On the way, `nevada.sonMet` (her first
              words to him) and `nevada.sonPinned` (the year pinned), and `nevada.bagDown` while her handbag is on
              the gravel. The penny goes into the tunnel for the Son (`g.send("penny", { to: "son" })`;
              `nevada.pennySent`) and waits there for the Rome end, which is the next stage's. It can be posted
              outside a talk too: the penny used on the little door, "One penny, for LUCK. In you go. ...Bye, penny!
              Say hi to my brother!"
Plants/pays:  Pays off the coin door in Rome (the Son kept it open), "Why is the sky DOWN?", the chickens Little
              Sister heard first, the timeline's red mark, and Mom's page: there are days when the correct thing to
              do is to make a scene, and this is the first of them. His tries are his own Rome (Walnut, the bank's
              cat asleep on the treasure, the doorkeeper who scores out of three, the counting man). Plants the
              warning: Dad went through and did not come (the second twist, at the end of Round One); the penny in
              the tunnel; and Grandpa Joe's "You tell me what you need, and I'll hold it", which #12 pays ("Mr. Joe?
              You said to tell you what I needed.") and #13 makes a promise of.
Notes:        The family's answer to the warning is in a word between Big Sister and her mother afterward: "Mother.
              He said not to go through." "He did, darling. Your father went through alone. We shall go through
              together. That is a different thing." "'It was,' she noted, 'not an argument. It was a decision.'" It
              is why the gate is "Hold hands. All the way through." Nothing in it is frightening: the Son is
              cheerful, fed, and holding a door open in the sun; his mother forgets her manners for a minute, and
              then she is his mother. Nothing in Act Two shows his end of it yet (the keys, the door held open):
              that is the next stage's. Hints: Mom, "That little door has a morning in it, and mornings have people
              in them. One of us should say hello."; Big Sister, "A door the size of a coin will carry a voice.
              Somebody should speak into it, clearly, and take notes."; Little Sister, "The Hummy Place has a HOLE
              in it now. I'm going to say HELLO into it. REALLY loud."
              How it is staged (LETTER-17): Mom kneels at KNEEL (600, 578), facing the door, her face at its height:
              `figure.kneel()` (js/art/rig.js `kneelPose`, kept to her: DESIGN.md, section 4), up on her knees, or
              sat back on her heels (`kneel("back")`) from her understanding until "Have you eaten?". Whoever was
              speaking into the door, and anyone in her way, makes room; at her understanding the girls stand either
              side of her, Big Sister behind her shoulder (560, 564) and Little Sister by the door (624, 589). Her
              figure is drawn without its handbag while it is down, and the handbag is a drawn thing on the gravel
              (js/art/props.js `handbag`) at (578, 592); Ranger fetches it from (558, 592), in his reach frames, and
              Mom takes it from his hands with her pick.
```

```
Puzzle #12: Something That Shines Like A Station Wagon        (Nevada · Lead: Big Sister, then anyone · the store, the glass)
Needs:        #9 and the letterbox; and the sun shade needs #11
Setup:        A coin's worth of light, a coin's worth of door. Big Sister has the rule (the end of "Some when"):
              a bigger shine, a bigger door. They need the biggest shine for a hundred miles.
Wrong tries:  Mom's car, looked at (once, after #9) -> "It's a sensible teal sedan. It has never shone in its
                                              life. That was rather the point of it." Big Sister: "Also, the
                                              hubcaps are plastic. I checked." Little Sister: "I could WASH it."
                                              "With what, sweetheart?" "...Lemonade."
              The banjo (the half-answer) -> Mom, in Grandpa Joe's talk: "Sir, might I ask you, very nicely, for
                                              the loan of your banjo?" "Nobody holds this banjo but me and the
                                              Lord, ma'am. But I'll stand where you tell me and play what you
                                              like." He gets up, slowly, a hand to the small of his back, walks to
                                              the corner of the glass, and plays, on his feet, facing the sun. The
                                              chrome at the end of the banjo's neck catches the low sun, the flash
                                              falls on the place, and the door grows: not to a coin, not to a car:
                                              to a banjo. "I could FIT!" "No." "I could fit SIDEWAYS." "No." Big
                                              Sister: "Bigger shine, bigger door. That is the rule, and it is now a
                                              fact. We need the biggest shine for a hundred miles." "Thank you.
                                              That was very... loud. You can sit down now." "...Most folks just
                                              say they liked the tune." He stops, the door shuts back to a
                                              coin, and he goes back to his chair (`nevada.banjoTried`). The girls
                                              can ask too, and he sends them to their mother: "Your ma asks me nice,
                                              little miss, I'll play it anywhere she likes."
              The hubcap wall, in the store -> Grandpa Joe, from the porch, through the window: "Them's not for
                                              sale, ma'am. Them's a COLLECTION." (To either of the girls: "Them's
                                              not for sale, girls. Them's a COLLECTION.") Jolene: "Forty years of
                                              other people's bad luck. He dusts 'em." Big Sister: "One hubcap is
                                              one hubcap's worth of shine. Less than a banjo. Nobody is taking a
                                              hundred and twelve."
              The space blanket, on the survival shelf -> Big Sister: "It would flash like a flag in a wind. There
                                              is no wind." Mom: "And three of us holding corners is three of us
                                              not going anywhere."
              The chrome polish, on the auto shelf -> "Chrome polish. 1987." "It's had since 1987 to decide what it
                                              wants to polish. Nothing here wants polishing."
              The sun shade, before #11   -> Jolene's three answers (#11's setup): "...A store with an empty
                                              window is a shed."; "Not the window, sugar. Anything but the
                                              window."; "...You do somethin' about my girls, and we'll see."
                                              (Asked at the window or across the counter, it is one count.)
              The sun shade at the glass before the Son has been heard -> the letterbox's hint.
Solution:     The sun shade in the front window: the folding silver kind, a windshield wide, DISPLAY ONLY, one
              side bleached by forty summers and the other as bright as the day it came. After #11, ask Jolene for
              it, at the window or in her talk: "Take the window. The window likes you." She comes out from behind
              the counter, lifts it out of the window and gives it to whoever asked. Mom: "Your father bought one
              of these for the trip. He said it was for keeping the car cool. I said it was for show." Big Sister:
              "It is a mirror the size of a windshield, Mother." Mom: "...Then it was for this." Then, at the
              glass, once they have heard the Son: Mom asks Grandpa Joe in his talk, "Mr. Joe? You said to tell
              you what I needed." (or the shade is taken to the glass, or held out to him: the same lines). Big
              Sister: "It wants holding in the low sun, square to the place, by somebody who is not going
              anywhere." "I been holdin' things for Jolene since 1974, ma'am. I can hold a sun shade." He gets up
              out of the rocking chair, slowly, a hand to the small of his back; whoever has the shade hands it to
              him at the corner of the glass; and he holds it up, square to the sun. The flash is the size of a
              windshield, and so is the door: it opens from the coin outward, to a doorway from the sand to higher
              than Mom's head and as wide as the two girls side by side. "It's GROWING! It's bigger than a banjo!
              It's bigger than MOMMY!" "'The door,' she noted, 'was exactly as wide as a windshield. She had never
              been so glad to be right.'" "And there's a different morning on the other side of it. ...Well. We
              knew that."
Gives:        A door the family can walk through (`nevada.wideOpen`). The sun shade stays in Grandpa Joe's hands,
              and the door stays open while it is held: he stands at the glass holding it, his chair empty, until
              the cut-scene.
Plants/pays:  Pays off the old man's story ("a flash... like a signal mirror... the sky opened up"), the coin
              (#9), and the rule of the doors, which the family now has whole and nobody told them. Pays off Act
              One without anyone knowing it: Dad opened his door with the wagon's windshield shade; his family
              opens theirs with a windshield shade from a gas station, and his wife's line about it. Pays off
              Grandpa Joe's word to Mom at the letterbox ("You tell me what you need, and I'll hold it."): she asks
              him by it. Plants Grandpa Joe holding the light when Jed makes his call, and letting it down.
Notes:        Hints: Mom, "The flash Mr. Joe saw came off a whole car. Ours came off a coin. Somewhere at this
              store is something that shines like a car."; Big Sister, "Bigger shine, bigger door. The biggest
              shine for a hundred miles is in that window, and Mrs. Jolene is fond of her window."; Little Sister,
              "The shiny thing in the WINDOW! Grandma Jolene said I could have anything. I did the chickens." The
              beat needs #11 as well as #9, so that her hint is true when it is given, and the letterbox too, so
              that the Son's warning comes before they go through. The door's three sizes are two of the engine's
              portals: the coin's, and over it a second, opened round at about a third of its size for the banjo
              and squeezed to a doorway for the windshield, bending the held shade with the sand. While he holds
              it Grandpa Joe can still be talked to (not about the banjo: his hands are full), and looked at ("Mr.
              Joe has not moved an inch, darlings. His arms must ache, and he will never say so."). The wide door,
              looked at: "It is open, it is wide, and it will not stay that way. A door is only open while the
              light is held." (Mom's car is painted teal, and her lines say so: DESIGN.md, section 14.) Round
              seventeen (LETTER-17): Mom's lines here loosened, as the pass asks: contractions with her girls, "Mr.
              Joe" for "the gentleman", and fewer "darling"s; every clue of the puzzle as it was.
```

```
Puzzle #13: Going Out And Coming In        (Nevada · Lead: any of them · the door)       THE GATE
Needs:        #12
Setup:        The door stands open and Grandpa Joe is holding the light on it. Nothing stops them now except
              goodbyes, which take a seven-year-old some time.
Wrong tries:  The door, before #12         -> too small: "Not yet, girls. It's a door for a coin, and there are
                                              three of us." / "It is the size of a coin. I am not." / "I could
                                              fit my HEAD. ...Mommy says not head first."
              Going through without the coin (whoever goes first must be carrying it) -> Mom: "The coin comes with
                                              us. It's the only thing we own that's been where we're going."
              Going through while Mom or Big Sister is still some way off -> Little Sister: "Everybody COME ON. The
                                              door's open and it's RUDE to keep a door open." And they come.
Solution:     Use the door (or the coin on it) as whoever is being played and has the coin; the other two come. They
              stand in a row in front of it, Little Sister in the middle. Goodbyes first, each in her own way.
              Little Sister, turned to the porch: "Bye, Grandpa Joe! Bye, Ranger! Bye, Grandma Jolene! Bye Darlene
              Charlene Marlene Arlene and Doreen! Keep GUARDING!" Grandma Jolene comes out of the shop's door onto
              the porch, under the hat of the visit, for Big Sister's: "Thank you for the window, Mrs. Jolene. And
              it takes a hen a whole day to make one egg." "Then that egg your sister's carryin' is a whole day's
              work, sugar. You mind it for her." "...I will think about that." She goes back in. Mom, to Grandpa
              Joe, with her hand out: "Thank you. For the lemonade, the story, and the light." And the two of them
              (round seventeen): "Will you be all right? Out here?" "Ma'am, I'm the only one on this porch who ain't
              goin' anywhere." "If we're not back..." "Then I'll be right here. Porch light on. However long it
              takes." "Go on, ma'am. 'The LORD shall preserve thy going out and thy coming in'..." Mom finishes it:
              "...'from this time forth, and even for evermore.' ...We said that at our own front door last night."
              "Then you're all right. Go get your boy." She turns to the door. "Girls. Hold hands. All the way
              through." They walk into it together, Little Sister in the middle, and each is gone as she reaches it.
              Then the cut-scene.
Gives:        `nevada.left`: the end of Act Four, and the cut-scene "Backup", which hands the game to Act Five.
              Where the family comes out is the next stage's (decision 1).
Plants/pays:  Pays off Psalm 121:8 as it was said at the front door (Act Three #11: "Going out, and coming in. All
              five of us."): a stranger at the end of the road has it by heart. Pays off his word at the letterbox
              ("You tell me what you need, and I'll hold it."), and plants his promise, "Porch light on. However
              long it takes.": the line the rest of his part of the game keeps. In the limousine, with his hands
              tied, it is the first thing he says to Ranger when the suits cannot hear (`limo.promise`: "I made that
              lady a promise, partner." "..." "I know. Then we'd best get loose."), and at the very end of the game
              it is what he does. The egg goes with Little Sister, and the coin with them; the sun shade stays with
              Grandpa Joe.
Notes:        One verse only, King James Version, letter for letter: Grandpa Joe says it to "coming in" (and his
              quotation marks close without a stop, since the verse runs on), and Mom finishes it from "from". The
              two halves are the verse exactly. Round seventeen (LETTER-17): Mom no longer says the reference (the
              author's rule of 16 October: a reference aloud only where it is natural), and Grandpa Joe's "Jolene's
              got it on a plate in the kitchen." went, so that after his promise and his half of the verse he does
              not say a third line before she answers; "Places, girls." is no longer said here (it still is at #9).
              The goodbye with Jolene was the design's "A hen cannot count to five": that fact was not used (a chick
              can tell small numbers apart), so Big Sister restates another of her corrections, and Jolene, as
              always, is right about the person. Hints: Mom, "The door's open, and Mr. Joe is holding the light.
              Goodbyes, girls, and then we go."; Big Sister, "The door is as wide as a windshield, and it will not
              stay that way. Say goodbye, and go through."; Little Sister, "The door's BIG now! Say bye to EVERYBODY
              and GO! Grandpa Joe's arms are getting TIRED." A game saved after they have gone through and before
              the cut-scene has played plays the cut-scene when it is loaded.
```

```
Cut-Scene: Backup        (closes Act Four and opens Act Five; the author's script, staged)
```
The family is gone; the door stands open in Grandpa Joe's light; the lot is quiet. Jed, who has
been pacing the fence since #7, turns round. He sees the door, walks up to it slowly along the far
side of the glass (two steps, a stop, two more), and says, in the author's words: **"Houston, we
have a problem...they figured it out. I need a cheeseburger and backup... immediately."** Grandpa
Joe lets the sun shade down, and is on his feet with his banjo again. The door folds shut, from the
outside in: to the coin, to nothing. Jed turns to him, and makes for the road round the end of the
glass; Grandpa Joe steps into his way and says the author's line, **"You ain't goin' nowhere flat
foot!"** The banjo goes up, and comes down over Jed's head: one twang, every string at once, and
Jed sits down in the dust with a puff of it, his sunglasses crooked and the banjo's hoop round his
neck like a collar. Nobody is hurt. Jed, from the ground: "...I would still like the cheeseburger."

Dust on the road: a gray limousine comes down the far road toward us, small, with a trail of dust,
turns off out of sight, and comes in along the front of the lot from the left, as long as the
porch, and stops in front of it. Four doors at once. Four men in gray suits, black sunglasses and
earpieces step out in a row, one of them with a paper bag. The first one, to the lot in general:
**"Who ordered a cheese burger? Jed? JED?"** They look round, and find Jed on the ground and
Grandpa Joe with what is left of the banjo. A pause in which four men consult a clipboard. "Sir. We
are going to need you to come with us." "Mind the hat." He walks over to them himself: nobody is
pushed or pulled. "We are minding the hat, sir." The four of them stand round him in a row, their
backs to us, and tie him up: "Sorry about this, sir. Regulations, sir." "Is that too tight, sir?"
"Snug as a hug, son." When they step back he is tied, with a bow. "And a bow, sir. Lifting on
three, sir. One. Two. ...Sorry, sir. Three." Two of them carry him to the car between them,
upright, his hat on and his boots off the ground: "Mind the... well. Mind what's left of the
banjo." "The banjo is evidence, sir. You will receive a receipt." In he goes, at a back door.
Jolene comes out onto the porch, under the hat of the visit: "JOE! You bring that banjo back in one
piece!" "Too late, Jolene!" "Then bring YOU back in one piece!" "I'll do my best!" Ranger comes out
from behind the car at a run, along the front of the lot, and in at the last door as it shuts. "Is
that a raccoon?" "I can neither confirm nor deny the raccoon." Two of them help Jed up, the hoop
still round his neck: "Is that my cheeseburger?" "Lunch rides in the back, sir. Regulations."
"...Of course it does." Jed gets in at the front, and the rest after him. The limousine turns, and
out of the window: "Jolene! Feed the hens! And don't sell my rocks!" "I'll sell every one of 'em,
Joe!" It drives out the way it came. Out back of the store (a close look, through its back door),
the five hens turn round, all together, to look the way it went; then they turn back to the fence.
Jolene, alone on the porch, to nobody: "Well. I'd better change my hat." She goes in. A card:
*"Meanwhile, in a limousine."*

Then the game passes to the new team, Grandpa Joe and Ranger, in the back of the limousine
(`nevada.backup`, and Act Five). Skipped (Escape, or Skip), the cut-scene runs to the same end at
once, and the limousine's opening then plays as itself. It is a beat of Act Five's
(`js/content/acts/limo.js`), played on the roadside.

How it stays silly: nobody is pushed, pulled or shouted at; the suits say sir and sorry; the
rope has a bow; the seatbelt is over the ropes in the next scene; Jed's injury is a banjo
collar and a wish for lunch; Grandpa Joe is cheerful from the first word to the last, and so is
Jolene, whose only worry is the banjo; Ranger chooses to go; the hens watch. "Come with us" is
answered on the spot by "Mind the hat."

*How it was staged* (the builders' choices; the design left them open, or asked for what has no
picture yet): the limousine has no pictures with its doors open, so the four step out from behind
it at its four doors, and get in by stepping behind it; Jolene shows over its roof, at the store's
door; the hens' look is drawn close from the store's own pictures, over the lot, for three seconds,
and the cut-scene does not go into the store; Grandpa Joe is carried upright between two of them,
not laid across them like a sofa; Jolene has no spatula. From the swing until he is tied, Grandpa Joe holds
what is left of the banjo, its neck.

**Also in the store, for character and nothing else.** Each of the three has a line for every
thing, and Jolene has a word for most, the first time anybody looks (`nevada.store.<thing>.<who>`,
`nevada.jolene.<thing>`): her greeting as they come in, under the hat of the visit
(`nevada.jolene.hello.1` to `.5`: "Well, hey there, sugar! Come in out of the sun. I'm Jolene.
Joe's out front pretendin' he ain't nosy. Ranger don't pretend."); the hat rack (Little Sister notices the hat
every visit, a line for each hat; Big Sister refuses to: "I am not going to say anything about the
hats. Any of the hats. I have decided."); the register (it rings for her and nobody else: "It knows
me, sugar. We've been together since '74. Longer than Joe and me, by a week."); the pickled eggs
(Big Sister declines in three languages: "No, thank you. Non, merci. Nein, danke."); the
take-a-penny dish; the postcards; Ranger's basket; the front window and the sun shade in it (before
and after #11); the spinner rack; Harold the cooler (Little Sister: "It's HUMMING. Is it a door?
...No. It's just cold. The Hummy Place is warmer."); the grill and the hot dog roller ("Grill's
been cold since 1979, sugar. The roller turns for company."); the rock bins (Big Sister: "One is
labeled 'SHY. Do not look at directly.' I am looking at it directly. ...Nothing. I am slightly put
out."); the map rack ("A road map of Nevada. It stops here too."); the auto shelf; the survival
shelf (Mom: "Water, jerky and a space blanket. Nevada is the driest state in the Union,
girls."; she buys three waters: "And three waters, please, Mrs. Jolene. We are going somewhere with
no shops."); the TV ("It's a weather channel, sugar. The weather's snow."); the pay phone, which
she answers ("Last Stop, Jolene speakin'. ...No? All right then." "Keeps it hopeful."); the
bulletin board; Jolene's chair and her knitting ("For Doreen. She feels the cold."); the hubcap
wall; the ceiling fan; the back door (Mom sees what the hens see: "They're looking straight at it,
girls. Straight at the place where the tracks stop."); and the door to the lot, and its bell,
Bernice. On the lot, the shop's door and the spare hat on its nail have a look from each of the
three too (`nevada.porch.door.<who>`, `nevada.hatnail.<who>`).

---

# Act Five opens: Everybody's Grandpa

<!-- NEVADA-12W: new in round twelve. -->
The inside of a gray limousine, driving. The first part of the game played by somebody who is
not family, and the first part played by a raccoon. The demo ends at its card (decision 11). <!-- SCENES-17 -->Since round
seventeen the card leads into the Office, and the demo ends there, at the end of its stage one (below).
The act is `js/content/acts/limo.js`; its first beat is the cut-scene "Backup", above, on the
roadside, and the rest is one scene, `nevada-limo`. Play it: `index.html?scene=nevada-limo&lead=grandpajoe`
(add `&flags=limo.arrived` to start after the opening, and `limo.loose` too for #15).

## The team

Grandpa Joe and Ranger are a party of two, the way Mom and the girls are a party of three: two
portraits at the top left (keys 1 and 2), switch at any time, each with pockets of his own
("Grandpa Joe's bib pocket", "Ranger's stash"). What each can do is the puzzle. Grandpa Joe is
belted to the long seat for the whole act, tied or loose, and never leaves it ("Regulations."): a
click on the floor does nothing for him, and he does everything from where he sits. Ranger has the
carpet between the seats, and fetches across the car what Grandpa Joe cannot reach.

| | What only he can do | What he cannot do |
| --- | --- | --- |
| **Grandpa Joe** | Talk: to the suits, through the divider, and to Ranger. Hum. Once his hands are free: eat, drink and read whatever Ranger brings him. | With his hands tied, nothing with his hands. Leave his seat. He does not hit anybody with anything again: the banjo was a once. |
| **Ranger** | Paws: nibble, reach, open, carry small things across the car, hop up onto the seat. He feels a thing with his paws. He never speaks: his line is always "..." (or "...!"), and Grandpa Joe says what he means. | Talk. Be told to leave a pickle alone. |

Trying a job as the wrong one is the hint, as in the house: Grandpa Joe at the ropes, "I'd need
hands for that, and mine are busy bein' tied."; Ranger at the divider, "..." and Grandpa Joe: "He
says they wouldn't understand him. He's right. They don't understand ME." What they say to each
other is `limo.talk.*` ("You didn't have to come, partner." "..." "He says where I go, he goes.
Even in a limousine. Especially in a limousine."; and, from Ranger, "..." "I know, partner. I miss
her too. She'll be changin' her hat about now.").

## Cut-scenes and puzzles

```
Cut-Scene: Meanwhile, in a limousine        (opens the act)
```
The back of the limousine, the desert going by both windows. Grandpa Joe sits at the far end of
the long seat, in the ropes, with a seatbelt over them. From the front, through the divider:
"Seatbelt, sir. Regulations." The divider slides down: the backs of two heads with earpieces, and
two pairs of dark shades in the mirror. "Sir, you are being transported for questioning." "Son, I
been questioned by a seven-year-old this mornin'. You ain't got anything she didn't." "...Noted."
The divider slides up. Ranger comes up from under the facing seat, by the little fridge, with the
mirror shades on: "Well, there you are. I wondered who'd got in." Then: "All right, Ranger. You
know what to do." Ranger crosses the carpet and sits up facing him: "...". He looks at the ropes,
and the play begins: "Play as Grandpa Joe or Ranger: use the portraits". From now until the first
strand is chewed, the divider goes down now and then by itself, as a suit looks back, and up
again.

```
Puzzle #14: Ranger's Ropes        (Act Five · Lead: Ranger, with Grandpa Joe · the long seat)
Needs:        the opening
Setup:        Four strands of regulation rope, a bow, and a raccoon with teeth. The trouble is the divider:
              every so often it slides down and a suit looks back. When the divider is down, Ranger must be a
              raccoon doing nothing; when it is up, and nobody in front wants to look back, Ranger must be
              furious.
Wrong tries:  Ranger at the ropes while the divider is down -> he hops up onto the seat beside the bow and
                                              chews, and is caught at once: "Sir, is the raccoon... chewing?"
                                              "He's groomin' me, son. It's affection." He gets down, and the
                                              divider stays down longer. (Nothing is lost.)
              Ranger at the ropes while it is up, with nobody singing -> a suit looks back halfway through the
                                              chew (the divider slides down): caught, the same.
              Grandpa Joe at the ropes     -> "I'd need hands for that, and mine are busy bein' tied." (And at
                                              the juice box and the clipboard.)
              Grandpa Joe at the divider   -> if it is up he raps on the glass, and it slides down: "Sir?" Then
                                              he talks (`dividerTree`): where they are taking him ("Where you
                                              boys takin' me, anyhow?"), the office ("What outfit are you boys
                                              with, anyhow?" "The Office Of Peculiar Sectors, sir. O. O. P. S."
                                              "Oops." "It is pronounced O. O. P. S., sir." "That's what I
                                              said."), what about ("Sir, we are not permitted to tell you what you
                                              will be asked." "Then how'm I supposed to get my answers ready?"),
                                              the regulations ("You boys got a rule for everything?" "Sir, the
                                              regulations cover every situation, sir." "Got one for a raccoon?"
                                              "...We are looking it up, sir."), and Jed's lunch ("And where's
                                              Jed's cheeseburger got to?" "Lunch rides in the back, sir.
                                              Regulations." Jed, from the front: "...I would still like the
                                              cheeseburger. For the record."). Talk does not put the divider up:
                                              "Y'all mind puttin' that window back up? I'm shy." "Sir, we are
                                              required to maintain visual."
              Ranger at the car phone      -> he lifts it, and it says nothing. "..." "That ain't for you.
                                              That's for later."
              A click on the floor, as Grandpa Joe -> nothing: he is belted in.
Solution:     As Grandpa Joe, at the divider: "You boys like music?" "Sir, we are required to..." "Hmm-hm-HMM,
              hm-hm-hmm... HMM-hm-hm-hmmm..." The divider goes up, and stays up while he hums: the Last Stop Rag,
              his own tune, plays under him, and three small notes rise over his head. "Sir, please stop
              singing." "Can't, son. It's a medical condition." Then, as Ranger, the ropes: he hops up onto the
              seat beside the bow and chews, "...!", one strand: "That's one. Keep goin', partner." The singing
              stops, the divider comes down once more, and Ranger sits on his work: "Groomin'." He gets down, and
              the divider stays down until Grandpa Joe sings again ("Sir, not again, sir." "Hm-HMM-hm-hm!
              Hmm-hm-hmm-HMMM! Hm. Hm. HMMMM..." "Sir. PLEASE, sir." "Still a medical condition, son. Flares up in
              limousines."; and after that, "Sir, we are asking you very nicely, sir." "Hmm-hm-hm-HMM-hmm-hm-hm-
              hmmmmm... Here comes the good part, boys! HMMM-hm!"). "Two. You're a credit to your mask." "Three.
              Easy, now. One to go." "Four! Now the bow. Gentle. It's a trade like any other." Ranger turns the
              bow over in his paws, and it comes undone: "...Well, I'll be. Hands. I'd near forgot I had 'em."
              He keeps the seatbelt on. "Regulations."
Gives:        Grandpa Joe's hands (`limo.loose`).
Plants/pays:  Pays off the author's scene: Ranger furiously nibbling the ropes. Pays off Ranger's paws
              (#10): the bow is a trade like any other. Plants the singing: the suits will do anything to
              make it stop.
Notes:        No song is sung, named or quoted: the Last Stop Rag is his own, and he hums it (`limo.sing.1` to
              `.3`; the tune is the same phrase his banjo plays on the porch). Afterward, Ranger at the ropes:
              "..." "He says he's keepin' the bow. It's his now." Hints: Grandpa Joe, "Them boys don't want to look
              at me. I just got to give 'em a reason."; Ranger, "..." (Grandpa Joe: "He says he knows exactly what
              to do and I'm in the way.").
```

```
Puzzle #15: Jed's Lunch        (Act Five · Lead: Grandpa Joe, then Ranger · the facing seat)
Needs:        #14
Setup:        On the facing seat, across the car: the paper bag (one cheeseburger, one pickle, cold), a juice box
              and the clipboard. Grandpa Joe cannot leave his seat, so whatever he wants from it Ranger fetches.
Wrong tries:  Grandpa Joe at the bag, before #14 -> "I can smell it from here. That's the cruelest thing they've
                                              done yet."
              Ranger at the bag            -> he is into it before anyone can speak. The pickle is gone.
                                              "Ranger. ...Well. He's earned the pickle."
              Ranger at the clipboard      -> he turns it over in his paws, which tells him it is a clipboard.
                                              "..." "He says it's a clipboard. He's right. That's all it is, to a
                                              raccoon."
              The juice box, as Grandpa Joe with his hands free -> Ranger fetches it, and he drinks it. "Apple.
                                              They're not monsters."
Solution:     As Grandpa Joe, his hands free, the bag or the clipboard. Ranger fetches the bag across the car to
              him (if the pickle is still in it, it is Ranger's fee, eaten on the way: "Ranger. ...Well. He's
              earned the pickle."), and then the clipboard. Grandpa Joe eats the cheeseburger while he reads:
              "Jed can have the next one." The clipboard, close: AREA CLOSED, ELEVATED RADIATION; a map with three
              sectors ringed in pen, 44, 1921, and the third under a thumbprint in mustard; a column headed WHAT
              OPENS THEM, its boxes empty; and in the margin, "A COIN?? Ask Houston." "'Area closed. Elevated
              radiation.' Same as the fence. And a map. Three sectors. Forty-four. Nineteen twenty-one." "And a
              third, with Jed's thumbprint square on top of it. In mustard. I ain't touchin' that." "And a
              column says WHAT OPENS THEM. Blank, all the way down. And in the margin: 'A COIN?? Ask Houston.'"
              "They got a map of holes and no idea how to open one." "And them little girls worked it out with a
              coin and a window." Ranger puts the map in the bib pocket for him: "That ain't stealin'. That's
              tradin'. They can have the banjo." The divider slides down: "Your receipt, sir. For the banjo.
              Regulations." It comes back to him through the divider. "'RECEIVED: one banjo (damaged). one raccoon
              (unconfirmed).'" "Hear that, partner? You're unconfirmed." "..." "He says he ain't never been so
              confirmed in his life."
Gives:        The map of the sectors and the receipt for the banjo, the first things in Grandpa Joe's pockets
              (`limo.map`); and the end of the demo. "That map's comin' home with us, partner. Somebody ought to
              know what opens them holes." "..." "He says the little girls know. He's right." The desert slows in
              the windows, and stops: "We're slowin' down. ...Well, would you look at that. Long name for a little
              building." The card: THE OFFICE OF PECULIAR SECTORS, and, smaller, "Desert Field Headquarters, the
              same afternoon". Then `limo.done` (the act's gate, `limo.end`), and the Office's arrival (below).
              <!-- SCENES-17: the card said "to be continued", and was followed by demo.done and the title screen; since
              round seventeen the demo ends at the Office's "Going Down". -->
Plants/pays:  Pays off the cheeseburger, three times: ordered, delivered, eaten by the wrong man. Pays off "they
              figured it out": the office has not, and Jed's margin says so. Plants the third sector (under Jed's
              thumb: decision 2) and the office itself.
Notes:        Hints: Grandpa Joe, "That clipboard's what they know, and that bag's what Jed wanted. I can read
              one and eat the other."; Ranger, "..." (Grandpa Joe: "He says the bag's his business and the
              clipboard's mine. He'll take the pickle for his trouble."). Every thing in the limousine has a look
              from each of the two (`limo.<thing>.joe`, `limo.<thing>.ranger`, and what Grandpa Joe says Ranger
              means, `limo.<thing>.ranger.joe`). The looks at the map and the receipt are written for all five of
              the family and the two of them, and nobody can hear them in this demo: both come into the bib
              pocket on the way to the last card. <!-- SCENES-17 -->(Since round seventeen Grandpa Joe looks at both in
              the Office, and Ranger, carrying the receipt there, thinks of Opal.)
```

---

# Act Five continued: the Office (stage one), "Processing"

<!-- SCENES-17: new in round seventeen. -->
The limousine stops at the Office Of Peculiar Sectors' desert field headquarters, the same afternoon: a very small
building with a very long name, a gravel lot, a flagpole, and on the roof an air conditioner much too big for it. The two
of them are split up at once, and each is played on his own. The stage ends the demo, on a card: LAMPLIGHTER, and
smaller, "to be continued". The design is `briefs/out/office-hq-design.md`, sections 3 and 4; the lines are
`js/content/lines/office.en.js` and the talks are trees in `js/content/talk/office.js` (WRITE-17's; their writer's
`ids.md` says when each line is said); the act is `js/content/acts/office.js` (act 6); the five scenes are
`js/content/scenes/office-lot.js`, `office-ducts.js`, `office-room.js`, `office-property.js` and `office-breakroom.js`, with
what they share in `office-common.js` beside them; and the two cut-scenes are `js/content/cutscenes/office-arrive.js` and
`office-down.js`. Play it: `index.html?scene=office-lot&lead=ranger` (the arrival plays first; add
`&flags=office.arrived` to start in the lot), or `index.html?scene=office-room&lead=grandpajoe&flags=office.arrived`.
What follows is the stage as the game plays it. Where the builders chose something the design left open, or staged it
otherwise, the card says so; the decisions are in [DESIGN.md](DESIGN.md), section 14 (94 to 122).

## The team, apart

Grandpa Joe and Ranger are still a party of two, with two portraits at the top left and pockets of their own, but from
the arrival on they are in two places at once: Grandpa Joe locked in Interview Room C, the Comfortable Room; Ranger
outside in the lot, and then in the air ducts. A click on the other one's portrait opens the Office's map, a blueprint of
the ground floor (white lines on blueprint blue, the duct dotted over the rooms, B-7 stamped RESTRICTED), with Grandpa
Joe's portrait in the Comfortable Room and Ranger's wherever he is; a click on him there drops into his scene, where he
was left. The map's only way is the lot to the ducts (by the intake); Grandpa Joe goes nowhere by it ("I'd go, but I'm
locked in. For my comfort."), Ranger goes into a room only through its grille (a thought: door, no), and B-7 answers
whoever clicks it (Grandpa Joe: "B-7. RESTRICTED. Ain't nobody invited me."; Ranger: down, no). Neither can finish
without the other: Ranger has the run of the building and no words; Grandpa Joe has words, a chair, an intercom and his
pockets, and cannot leave the room. They meet at the vent in the room's ceiling: with Ranger at the grille over it and
Grandpa Joe on the spare chair under it, they talk, and hand things up and down through the slats (a receipt fits, a pie
tin fits, a banjo does not).

| | What only he can do | What he cannot do |
| --- | --- | --- |
| **Grandpa Joe** | Talk to anybody: Dale and Merle, Opal, Houston on the intercom, Ranger at the vent or in the room. Stand on the spare chair and reach the vent. Read. Mend a banjo, and play it. | Leave the Comfortable Room: it is locked "for your comfort". Walk while they question him (he answers from his chair) or while he stands on the spare chair (anything farther off steps him down first). Lie: he will not, even to the Office; he asks, nicely, on somebody's behalf. |
| **Ranger** | Climb, crawl and squeeze; look down through a grille, drop down where there is something to land on and nobody looking, and climb back. Turn wing nuts and pull switches. Wash things. Eat a pie. Read a picture. Trade. | Talk: in the Office he thinks in pictures, and Grandpa Joe says what he means only where he can hear him. Carry anything bigger than a pie tin. Be on the form. |

**Ranger's thought pictures.** Every look and try of Ranger's is a small bubble over his head with one to three pictures
in it (`js/art/thoughts.js`, thirty-nine of them, drawn in the game's pixel style): pie tin, plus, banjo is a hint the
player can read. Where Grandpa Joe can hear him (in the Comfortable Room together, or with Ranger at the grille over it
and the suits gone) the bubble is followed by Joe's reading of it ("He says there's a pie. He says it ain't his. He says
that's a technicality."); away from Joe, the picture is all there is. The stock replies are the Office's own: Ranger's are
thoughts, and Grandpa Joe's are about the questionnaire first, then his own.

**The heat.** Once Ranger has turned the building's air off (#16), the Comfortable Room warms with the play time: 72
until then; 77 forty seconds later; 81 two minutes and ten seconds after the air went off (`office-common.js`: the
thermostat's three painted numbers, and the same in every scene and after a load, since it is worked out from the
moment of #16). At 77 Merle mops his forehead and Dale loosens his tie; at 81 the plastic plant droops ("That plant is
plastic, and it is wiltin'. I didn't know they could.").

**The speakers.** Houston is on every speaker in the building: the story's announcements at their moments (the arrival
and Wendell's pie, the raccoon, the air, the cheeseburger, the music, the music going down, the test), and now and then,
while the player has the controls anywhere in the Office, one of her others ("Dr. Fairweather to B-7, please." "The
Director's plant needs watering." "Reminder. Form 7 is not optional."). In the break room Jed talks to her in his
earpiece, and Wendell on the door reports to her by his.

## Puzzle structure

```
                 Cut-scene: A Very Small Building With A Very Long Name
                                         |
          +------------------------------+-------------------------------+
          |                                                              |
 #16 Not On The Form (Ranger, the lot)                 #17 The Comfortable Room (Grandpa Joe; a talk)
   the trash can, the drainpipe, the roof,                the questionnaire: yesterday at 1747, the
   four wing nuts, the fan switch                         green page, Opal, the receipt
   -> into the ducts; the building's air off  ---->       -> at 81, Regulation 9: he is alone
          |                                                              |
          +------------------------------+-------------------------------+
                                         |
                 #18 The Bearer (Grandpa Joe -> Ranger -> Opal -> Grandpa Joe)
                     the receipt up through the vent, and down through PROP & EFF's grille
                     -> the banjo comes back, damaged
                                         |
                 #19 Wendell's Pie (Grandpa Joe on the intercom; Ranger in the break room)
                     Jed's cheeseburger, on Jed's behalf; the pie, the clean tin, the schedule
                     -> the pie tin and the test schedule, down through the vent
                                         |
                 #20 A Soundproof Room (Grandpa Joe: the pie-tin banjo, the Rag, the suits)
                                         |
                 Cut-scene: Going Down  ->  card: LAMPLIGHTER, "to be continued"
```

Goal of the stage: **get out of the Comfortable Room, and find out what is going on.** The player learns, in this order:
that the Office has a thing called Lamplighter that the men upstairs are not supposed to read about (#17: the green
page); that it was fired yesterday at 1747 hours on Sector 1921, the minute the sky opened over Grandpa Joe's road, and
fires again today at 1700 on Sector 44, the boy's year (#19: the test schedule); and that it is on B-7 (the schedule, and
the suits' own words in #20). #16 and #17 can be played in either order and turn about: the interview can be had at once,
and only the heat ends it; and the heat is #16's.

The beats (`js/content/acts/office.js`, act 6, "Act Five, continued: Processing"), each with the fact it makes true:
`office.arrive` (the cut-scene, `office.arrived`: it needs `limo.done`), `office.inside` (#16, `office.inside`),
`office.room` (#17, `office.alone`), `office.bearer` (#18, `office.banjoBack`: it needs `office.inside` and
`office.alone`), `office.pie` (#19, `office.schedule`), `office.rag` (#20, `office.down`) and the gate, `office.end`
(Going Down, `office.done`; with it the demo's end, `demo.done`). The limousine's gate, `limo.end`, now leads into the
arrival. A long puzzle's hint follows how far it has got: Ranger's on the gravel is the can and the pipe (trash, plus,
up), on the roof the wing nuts, with the grille off the switch; Grandpa Joe's in the room follows the thermostat ("Them
boys don't like it warm. I seen 'em sweat in that limousine." at 77; "Eighty-one. If there's a regulation for that, now's
when I ask about it." at 81).

## Location layout

Five places, one painting each, all in Nevada's time and in one building, so Houston is heard in every one of them; no
way out at the edges of any. The lot and the ducts are joined by the intake on the roof; each room is reached only from
above, through its grille.

```
THE LOT (office-lot): outside, early afternoon, the desert behind; two floors, the gravel and the roof
+------------------------------------------------------------------------------------+
| the FLAGPOLE      THE ROOFTOP UNIT, the size of a minivan: the intake GRILLE with  |
| (its pennant)     four WING NUTS and the fan behind it, the maintenance SWITCH (a   |
|                   fan with a line through it on its sticker); in front, the ROOF    |
|                   +-------------------------------------------+                    |
| the GATE, and its | the SIGN: OFFICE OF PECULIAR SECTORS       |  the DRAINPIPE    |
| SIGN: PLEASE DO   | the WINDOW   the DOOR, the KEYPAD          |  (ends three feet |
| NOT LOOK DIRECTLY | WENDELL on the door; the MAT: WIPE         |  up the wall)     |
| AT THE BUILDING   +-------------------------------------------+  the TRASH CAN    |
|                                          the gray LIMOUSINE, its back door open    |
|  the DESERT          the gravel ..........................   Here: Ranger          |
+------------------------------------------------------------------------------------+
```

Two floors: the gravel, and the strip of roof in front of the unit, three metres up. Ranger goes between them only by the
can and the drainpipe; once the can stands under the pipe, a click on the other floor takes him up or down. Wendell
stands on the door facing the gate, by regulation, with a button on his lapel that says it is his birthday. The intake is
the way into the ducts, and the ducts' own intake brings him back out onto the roof.

```
THE DUCTS (office-ducts): a sheet-metal run over the ground floor, at Ranger's height, lit from below
+------------------------------------------------------------------------------------+
| the INTAKE: daylight     the INSULATION, the WATER PIPE and its VALVE,   the B-7    |
| from the roof, the       the WIRES; RIVETS along the back wall           SHAFT: the |
| INTAKE FAN                                                               big FAN    |
|   ...[ROOM C]......[PROP & EFF]......[BREAK]......[HALL]...  (four grilles)  across  |
|   a COFFEE CUP, a PENCIL, a sandwich WRAPPER, a LIFTED tile, a LIGHT FITTING and a it;|
|   caged BULB; the CEILING TILES under the duct                   its STENCIL: B-7 |
|  Here: Ranger, at the intake, lying at a grille, or at the shaft     EXHAUST ...   |
+------------------------------------------------------------------------------------+
```

He walks the middle of the duct's floor, on six marks: the intake, one over each grille, and the shaft. From each grille
he looks down into the room under it ("Look down": the room as it is, its people living their lives, seen through the
slats; only what answers from above is there to click), backs up (the corner button, Escape, or a click outside), and,
where there is something to land on and nobody looking, drops down ("Drop down"): ROOM C onto the spare chair's seat,
once the suits have gone and Grandpa Joe is not standing on it; PROP & EFF onto the top shelf, under the grille, where
Opal's back is turned; BREAK onto the top of the fridge (with Jed there, Jed shoos him back up). The HALL has no painting
in this stage: looked down through, it is the elevator the first time (door, down), nothing to land on after (down, no),
and then nothing doing (eye, zzz); "Going Down" is heard through it. The B-7 shaft is not yet his way: "not without Joe"
(joe, no). The ducts are being painted again this round so that they read better as the inside of a duct; the marks,
the walk, the grilles and the fan stay exactly where they are, and every other thing's shape comes from the painter's
layout in one block of the scene (decision 117).

```
THE COMFORTABLE ROOM (office-room): INTERVIEW ROOM C. THIS ROOM HAS BEEN RATED COMFORTABLE.
+------------------------------------------------------------------------------------+
|  the VENT, in the      the CLOCK    the SIGN, the THERMOSTAT (72), the INTERCOM     |
|  ceiling over the                   (DISPATCH. PRESS TO TALK.), the POSTER          |
|  corner                             (PECULIAR? REPORT IT.)                          |
|  the DOOR (locked      the long one-way MIRROR                the WATER COOLER and  |
|  "for your comfort")                                          its paper CONES       |
|  the SPARE CHAIR,      the TABLE and the QUESTIONNAIRE; GRANDPA JOE   the plastic   |
|  under the vent        in his CHAIR, DALE and MERLE across it         PLANT         |
|  Here: Grandpa Joe; Ranger from above, or dropped in onto the spare chair           |
+------------------------------------------------------------------------------------+
```

Grandpa Joe sits at the table while they question him and does everything from his chair. Alone, he walks, and climbs
onto the spare chair under the vent; standing on it he does everything from up there, and a click on the floor steps him
down. For Ranger the room has two floors: the floor, and the spare chair's seat, which he lands on from the grille and
climbs back up from. Dale's and Merle's chairs can be looked at once they have gone.

```
PROPERTY & EFFECTS (office-property): the back of the room, shelves to the ceiling, every thing tagged
+------------------------------------------------------------------------------------+
| the VENT, over the     ARCHIVE BOXES of FORM 7, by the decade   OPAL'S WINDOW onto  |
| top shelf              on the shelves  ; a ROMAN SANDAL (1951), the hall, its SIGN  |
|                        a CLAY LAMP, a TIN CUP, a HORSESHOE, a   and its BELL (on   |
| the SHELVES            COWBOY HAT bleached white, a GOOSE        the hall's side);   |
|                        FEATHER, a CASSETTE TAPE, a GARDEN GNOME  the COUNTER, her   |
|                        and on the lowest shelf, tag No. 3117,    DATE STAMP; OPAL   |
|                        the BANJO (damaged)                       on her STOOL, her  |
|                                                                  KNITTING; the DOOR |
|  Here: Ranger, looking down, or on the top shelf under the grille                   |
+------------------------------------------------------------------------------------+
```

Ranger's floor in here is the top shelf under the grille; the aisle is Opal's (a click on it: eye, no). Opal sits on her
stool at her window with her back to the shelves, knitting, and turns round once, the first time he lands: "...You are
not on the form, dear. Mind the gnome."

```
THE BREAK ROOM (office-breakroom)
+------------------------------------------------------------------------------------+
| the VENT, over the     the CLOCK    the CORKBOARD: FORM 7 IS NOT OPTIONAL; FOUND:   |
| FRIDGE (LABEL YOUR                  ONE ROMAN SANDAL; the BOWLING league; a TAKEOUT |
| LUNCH. MGMT.), its                  MENU; and the LAMPLIGHTER TEST SCHEDULE         |
| MAGNETS, a box of      the COUNTER: the MICROWAVE, the DISH RACK, the SINK,          |
| FORKS, a dusty PLANT   WENDELL'S PIE and its CARD, the COFFEE MAKER, PAPER CUPS     |
| the COUCH: FLOYD       JED in a plastic CHAIR, the ice pack on      the VENDING     |
| asleep (zzz)           his head and the hoop round his neck,         MACHINE, its   |
|                        looking right at the pie                      BUTTONS, TRAY  |
|  Here: Ranger, looking down, or on the fridge, the counter, the floor     the DOOR |
+------------------------------------------------------------------------------------+
```

Ranger has three floors in here: the fridge's top, the counter and the room's floor, joined by the painter's paths (the
fridge, the microwave, the counter; the counter's end, the floor by the machine). A thing used where it is takes him to
its floor by them, as a raccoon goes. Floyd sleeps on his regulation rest the whole stage, a thought of his own over him
(zzz), and says regulations in his sleep.

## Cut-scenes and puzzles

```
Cut-Scene: A Very Small Building With A Very Long Name        (opens the stage)
```
The limousine's card first, on black: THE OFFICE OF PECULIAR SECTORS, and smaller, "Desert Field Headquarters, the same
afternoon". Then the lot, and the stage's own title over it while the four suits get out of the car in a row: "Sir, we
have arrived, sir." "Sorry about the drive, sir." Two of them bring Grandpa Joe out of the back door, upright, hat on:
"Sir, you will now be processed." "Son, I been processed. Jolene does it every Sunday before church." Jed comes round
from the front with the banjo's hoop round his neck and what is left of the banjo in his hands, and goes in ahead:
"Evidence." "Careful with her, son. She's had a day." "...We have all had a day, sir." Across the gravel to the door
between the suits: "'Please do not look directly at the building.' Son, there ain't nothin' else out here to look at."
"Please look at the gravel, sir." "That's a powerful lot of air conditioner for a buildin' no bigger'n a garage." "Sorry,
sir. We are not permitted to discuss the air." He wipes his boots on the mat (WIPE): "Thank you for wiping your feet,
sir." "Sign asked nice." At the door he looks back at the limousine's open door, and says, not loud: "Ranger. You know
what to do." "Sir, was that addressed to the raccoon?" "What raccoon, son?" Dale checks the clipboard: "...The raccoon is
not on the form." "Then officially, there ain't one." The door shuts on all of them but Wendell, who turns round, by
regulation, to face the gate: "...It is my birthday." Inside, on every speaker: "Attention all personnel. One civilian
has arrived for processing. Please make him comfortable." "Attention all personnel. It is Wendell's birthday. There is a
pie in the break room. Do not eat the pie." A moment. Ranger comes out of the limousine's open door in his mirror shades,
drops to the gravel and sits up: a thought of Grandpa Joe's hat; a question mark; the door, plus a suit. Play as Ranger.
Grandpa Joe is in the Comfortable Room already (the game has put him there, on his chair at the table), and the player
can switch to him at any time. Ranger has his stash: one bottle cap, his best. Skipped, the cut-scene lands in the same
place.

```
Puzzle #16: Not On The Form        (Act Five, continued · Lead: Ranger · the lot)
Needs:        the arrival
Setup:        A raccoon outside a building he must get into. The front door has a keypad and Wendell. The rooftop unit
              is the size of a minivan and breathes in through a grille on its side, the fan turning behind it. The
              drainpipe on the corner would take a raccoon up to the roof, but it ends three feet up the wall. A trash
              can stands by the wall, its lid chained (REGULATION).
Wrong tries:  The door                       -> Wendell turns to him: "Sir. Er. Raccoon. You are not authorized." "Shoo,
                                                please." (no) He backs off a few steps. Again: "Raccoon. You are still not
                                                authorized." "I am asking you very nicely, sir. Raccoon." (heart: asked
                                                nicely, he goes; he likes manners)
              The keypad                     -> he presses every button, and it beeps every time: "That is not the code."
                                                (question); "That is also not the code."; "Sir. Raccoon. That is the code
                                                for the vending machine. Please stop."
              The mat                        -> he wipes his feet, all four, carefully (hand, shiny): "...Thank you for
                                                wiping your feet, sir. Raccoon."
              Wendell                        -> "Sir. Raccoon. Please do not approach the door." (no)
              The bottle cap, on Wendell     -> "Sir. Raccoon. That is a very nice bottle cap." "But this is my birthday
                                                button. It is not for trade." (bottlecap, heart)
              The drainpipe, from the gravel -> he stretches up; it is just out of reach (up, no); again (hand, up, no)
              The limousine                  -> he hops up onto the hood; the roof is too far (no)
              The intake, the fan going      -> he leans back from it (fan, no)
              The unit, from the gravel      -> (up, question); the gate, the sign, the flag, the window, the desert: a
                                                thought each, and no way in
Solution:     The trash can. He tries the lid (hand, no: chained), and tips the can over instead: a clang. Wendell turns
              round, and there is a raccoon in a trash can: "...One raccoon. In trash." "Noted." (paper, heart: he is on a
              form at last.) Wendell turns back to the gate, and a little later reports it into his earpiece: "Houston, it
              is Wendell. One raccoon, in trash. Noted." Houston: "Attention all personnel. One raccoon has been noted. In
              trash. It is not on the form. Carry on." Ranger rolls the can along to the foot of the drainpipe and stands
              it up there (idea), and climbs the can and the pipe to the roof (up, heart). On the roof: the four wing
              nuts, one, two, three, four (the low ones sitting up, the high ones climbing the grille's louvres; each one
              squeaks, and goes), and the grille comes off and leans on the unit; behind it the fan, turning. The switch
              beside it has a picture of a fan with a line through it on its sticker: he reads the picture, looks at the
              fan (fan, arrow, no), and pulls. The fan runs down and stops, and the building's hum with it. Houston:
              "Attention all personnel. The building's air is off. Will maintenance please see to it." "Wendell, you are
              maintenance." Wendell, into his earpiece: "Houston, I am on the door. It is my birthday." Houston: "Then the
              air will have to wait." He goes in at the intake, to find Joe (joe, heart); and in the ducts: where's Joe?
              (joe, question)
Gives:        Ranger in the ducts (`office.inside`), and the building's air off (`office.acOff`; its moment kept,
              `office.acOffAt`): from now on the Comfortable Room gets warmer.
Plants/pays:  Pays off a raccoon and a trash can (it had to be done). Plants the heat (#17) and the stopped fans (the B-7
              shaft, in Going Down). The switch's picture is where the game first says that Ranger reads pictures, which
              is how he thinks.
Notes:        A click on the gravel from the roof takes him back down the pipe, and the can, under it, back up. The
              switch, pulled again: (fan, no): the fans stay off. Hints: Ranger, on the gravel (trash, plus, up), on the
              roof (wingnut, hand), with the grille off (switch, fan, no), and with the air off, the open intake (door,
              heart); Grandpa Joe, once he is alone and Ranger not yet in: "Nothin' I can do from this chair. Gettin' into
              places is Ranger's end of it."
```

```
Puzzle #17: The Comfortable Room        (Act Five, continued · Lead: Grandpa Joe · a talk · the interview room)
Needs:        the arrival (the talk can be had at once; it is finished by #16)
Setup:        Grandpa Joe at the table, Dale and Merle across it with the questionnaire. Forty-seven pages. The door is
              locked "for your comfort". The thermostat on the wall says 72.
The talk:     `interviewTree`, with Dale or Merle. "Sir. Thank you for coming in, sir." "Didn't have a lot of say in it,
              son." "Sorry about that, sir." "This is the questionnaire, sir. It is forty-seven pages." "Sorry about that
              too, sir." Dale reads the questions, Merle writes the answers down in capitals and apologizes for each one
              before Dale asks it, and every answer is Grandpa Joe's choice, and every one is true:
                "Name?"            "Joe." "Last name?" He never says Grandpa; "Folks just call me Grandpa." / "It's on
                                   the sign out front of my store, son." ("The sign says GRANDPA JOE'S, Dale." "Then it
                                   is Grandpa, sir.") / "I'd sooner not say, son." Whichever way: "NAME: JOE. LAST
                                   NAME: GRANDPA." "...Jolene's gonna love that."
                "Occupation?"      "Lemonade." ("Sir, lemonade is a beverage." "It's a dollar, son.") / "Rocks." ("Sir,
                                   are you a rock?" "I sell 'em, son. Some days I feel like one.") / "Watchin' the road.
                                   Forty years."
                Yesterday at 1747: "I observed a station wagon." ("Sir, what color was the station wagon?" "Red, son. Wood
                                   on the sides." "Sorry, sir. There is no box for wood.") / "What's a sector?" ("We
                                   are not permitted to say, sir." "Then I can't rightly say if I seen one.") / "Son,
                                   I've told this office nothin' forty-one times. Ask Opal. She's got 'em all on file."
                                   ("She files them, Dale." "...She files them.") / and, once, "Seventeen forty-seven.
                                   That's an awful particular minute, son." (the clue: somebody wrote down the very
                                   minute)
                Page two, "Describe the raccoon." "What raccoon?" ("...The raccoon is not on the form, sir." "It is on this
                                   form, Dale. Page two, question one.") / "Handsome." ("Very handsome.") / "He's a lot
                                   like me, only he don't talk and he's better lookin'."
                The green page,    "Have you had any contact with Lamplighter?" "With what?" / "Son, I don't believe I've
                                   had the pleasure." / "That some kind of a lamp?" "Strike that, sir." "You read the
                                   green page." "I read the green page." "We are not supposed to read the green page."
                                   (the clue: there is a Lamplighter, and they do not know what it is either)
                The banjo,         "Did you strike an officer of this Office with a banjo?" "Once." ("Thank you for your
                                   honesty, sir.") And the receipt: "Your banjo has been entered into Property &
                                   Effects, sir. You have your receipt." "I do."
              And on and on: five more questions, round and round ("Have you ever been, or are you now, a sector?" "Not as
              I know of, son."; "Have you ever looked directly at the building?" "Your sign told me not to. So I did."), the
              last of them "On a scale of one to five, how comfortable are you?" "Four, son. Five if the door opened."
              ("Sorry, sir. That was the end of page two." "Page two, continued."). At any question he can ask to go home
              ("Sir, you have not completed the questionnaire." "How far are we?" "Page two, sir."), ask about the green
              page once he has heard of it, or ask for a minute ("Give me a minute"): the talk goes on where it stopped.
Wrong tries:  The door                       -> "Sir, the door is locked for your comfort." "...I'm feelin' better already."
              The thermostat at 72           -> "Seventy-two. Course it is." "It is always seventy-two, sir. It is the
                                                Comfortable Room."
              The spare chair, the intercom  -> "Sir, please remain in your chair, sir. That chair is the spare."; "Sir,
                                                please do not touch the intercom."
              The mirror                     -> "Afternoon. ...Go on and finish your chips, son. I won't tell." "Sir, that
                                                is a mirror." "Course it is, son." (His look at it: "That's a nice mirror.
                                                Somebody's back there eatin' chips.")
Solution:     After #16 the room warms, then gets hot. At 77: "Seventy-seven. And climbin'." "Within regulations, sir.
              Comfortable is seventy to eighty." "It is going up, Dale." "Then we will read faster, Merle." Merle mops his
              forehead; Dale loosens his tie a finger's width. In the talk, "Gettin' warm in here, fellas.", the same, and
              then "Still within regulations, sir. Just." At 81 the plastic plant droops, and either the thermostat
              ("Eighty-one. Now that ain't comfortable."), or in the talk "Hot in here, fellas. Ain't there a regulation?"
              at any question, or, at the last question, his honest "One, son. And that's bein' neighborly." ("Dale. That
              is a one." "...There is a regulation for a one."): "Regulation 9. 'The Comfortable Room shall be
              comfortable.'" "It is not comfortable, Dale." "...Then the interview is suspended, pending a Form 30."
              "Sorry, sir. We will be back, sir. A Form 30 is very long, sir." "The door will be locked for your comfort,
              sir." They gather the questionnaire, apologize their way out and lock the door. Grandpa Joe alone: "...Well."
              A short prayer of his own: "Lord, You know where that family is, and I don't. You look after 'em." "...And
              that raccoon of mine, wherever he's got to." He gets up, and looks up at the vent.
Gives:        Grandpa Joe alone in the room (`office.alone`): the spare chair under the vent, the intercom.
Plants/pays:  Pays off the limousine's "Sir, we are required to..." at full length. Plants Lamplighter (the green page),
              the minute of yesterday's opening, Opal (who files his nothings) and the intercom (#19). Merle writes his
              name GRANDPA, and Houston calls him "Mr. Grandpa" from then on.
Notes:        The questionnaire's place is kept (`office.iv`): a talk broken off goes on at the question it stopped at.
              The hint follows the thermostat (72, 77, 81). Ranger's, while Joe is in there: (joe, hot).
```

```
Puzzle #18: The Bearer        (Act Five, continued · Lead: both · the room, the ducts, Property & Effects)
Needs:        #16 and #17
Setup:        Grandpa Joe wants his banjo. A banjo will not come through a vent, and he cannot leave the room. He has the
              receipt: "'RECEIVED: one banjo (damaged). one raccoon (unconfirmed).' I aim to collect."
Steps:        Ranger at the grille over ROOM C, the suits gone: he looks down, and Joe hears him: "...!" (heart, the first
              time he looks); and with the suits gone, "Comin', partner. Let me get up on that chair." Grandpa Joe stands
              on the spare chair under the vent ("Easy, now. ...I ain't stood on a chair since Jolene saw a mouse.", if he
              climbs up himself). At the vent, the two of them (`ventTree`): "Well, there you are. You got in." (fan, no)
              "He says he turned the fans off. ...So that's why I'm cookin'. Partner, you're a wonder." "Partner, I want
              my banjo back." "Them boys'll do anything to make the Rag stop. With a banjo, I could empty this whole
              building." (banjo, door, no) "He says a banjo won't come through there. No, sir. But a receipt will." Then
              the receipt: "Property and Effects. A little window with a bell, and a lady with glasses on a chain." (opal,
              question) "That's her. Opal. You give her this, and she'll know what to do." (or, if Ranger has looked down
              into Property already, (opal, idea) "You seen her already? ...'Course you have.") "Up she goes." He
              pushes it up through the slats (receipt, heart). Or the receipt used on the vent does the same.
              Ranger takes it along the duct to the grille over PROP & EFF and looks down: Opal at her window with her
              back to the shelves, and on the lowest shelf, tag No. 3117, the banjo (shiny, shiny, shiny, the first
              time). The receipt used on the grille, or on Opal or her counter from the top shelf: it goes down through
              the slats (receipt, arrow, opal), flutters along the aisle and lands on her counter (receipt, heart). Opal
              reads it, close, through her half-moons: "Claim number 3117. One banjo, damaged. One raccoon, unconfirmed."
              She turns on her stool until the vent is above her; two eyes in a mask look back. "...Confirmed." THUNK,
              with the stamp. "Regulation 4. Property is returned to its owner on presentation of the receipt." "It does
              not say who presents it." "Thank you, raccoon." (opal, heart) She gets off her stool, takes the banjo off its
              shelf, and goes out with it, and her keys. Ranger hurries back along the duct to ROOM C's grille, and the
              game goes to Grandpa Joe.
              The key in the door, and Opal with the banjo in her arms. "Opal, of Property and Effects. Same glasses on the
              same chain since 1971." (and up in the vent, opal, heart) (`opalTree`) "Afternoon, Joe." "Opal." "A raccoon
              brought me your receipt." "He's good like that." "Sign here." He signs; THUNK. "Forty-one statements of
              nothing, Joe Hollis." "I'm a man of few observations." "It's warm in here." "It's the Comfortable Room."
              "One banjo, damaged. Returned to its owner." She puts it in his hands. "Well. Look at you, darlin'." She
              looks up at the vent: "...And good afternoon to you too, up there." Then as many words as he likes: what they
              did to her ("Jed's head went through her, Joe. It's in the report." "Rim: sound. Neck: sound. Strings: sound.
              Head: gone."), how Jed is ("In the break room, with an ice pack and the hoop still on. He says it's
              evidence."), the Roman sandal ("Since 1951. The Director brought it in himself, and he has never once come to
              claim it." "Maybe he don't want it back." "Everybody wants something back, Joe. That's what my window is
              for."), Lamplighter ("That's a green-page word, Joe." "I file the green pages. I have never read one. Reading
              is a different department."), the door ("Regulations, Joe." "I figured." "But I'll lock it gently."), and
              "Thank you kindly, Opal." "Regulation 4, Joe. Thank the raccoon." "Regulations, Joe." She locks the door
              behind her, gently.
Wrong tries:  Ranger at the banjo, on the top shelf -> he cannot lift it (banjo, up, no); and it would not fit in the duct
                                                anyway (banjo, door, no)
              Ranger at Opal's bell          -> it is on the hall's side of the glass (hand, no)
              Ranger at the tagged things    -> (paper, no): every one has a tag, so it is somebody's
              Anything else on Opal, or down the grille -> (no): he keeps it
              The aisle, from the shelf      -> (eye, no): she would see him
              Grandpa Joe on the chair, nobody at the vent -> "Ranger? ...Nope. Just me and the duct." "Ranger? ...Still
                                                just the duct. It don't say much either."
              The vent from the floor        -> "Can't reach it from down here. I'd want somethin' to stand on."
              The map, the receipt, the banjo up the vent -> "Not the map, partner. That map's comin' home with us."; "She
                                                won't go through there, partner. That's the whole trouble."
              Ranger handing the receipt or his bottle cap down to Joe -> "That ain't for me, partner. That's for Opal.";
                                                (bottlecap, heart, no) "He says that's his best one, and it ain't for
                                                givin'. He'd trade it, for the right thing."
              Ranger dropping in while Joe stands on the chair, or while the suits are there -> (eye, no); (suit, no)
Gives:        The banjo (damaged) (`office.banjoBack`), in Grandpa Joe's hands.
Plants/pays:  Pays off the receipt from the limousine (and its "one raccoon (unconfirmed)", now confirmed and stamped).
              Plants Opal for stage two (her keys, and the Director's sandal on her shelves). The only time his surname is
              said.
Notes:        The cut to Grandpa Joe is the story's, as the cut to the limousine was: the player has the controls again at
              Opal's door. The two of them can talk at the vent at any time after (the vent's tree; and from above, a click
              on Joe is a word between them: (joe, heart) "Missed you too, partner."). Hints: Grandpa Joe, "That receipt
              says one banjo. Opal'll honor a receipt. I just can't walk it down the hall.", then "Ranger's got the
              receipt, and Opal's got the banjo. Rest of it's up to him."; Ranger (joe, down), then (receipt, arrow, opal),
              with Joe's reading at the vent.
```

```
Puzzle #19: Wendell's Pie        (Act Five, continued · Lead: both · the room's intercom; the break room)
Needs:        #18
Setup:        The banjo's head is broken: "Somethin' round and tin, stretched tight. A pie plate'd do it, if a man had a
              pie." Ranger, at the grille over BREAK, looks down: Floyd asleep on the couch (zzz), Jed in a plastic chair
              with an ice pack on his head and the hoop round his neck, facing the counter; and on the counter, a pie in
              a tin, with a card: HAPPY BIRTHDAY WENDELL. DO NOT EAT. (REGULATIONS). Jed is looking right at it ("I am not
              going to eat the pie." "It says do not eat. It says it in capitals.").
Steps:        1. Jed has to go. Ranger cannot make him: dropping in with Jed there, "Raccoon. In the break room." "...Do
                 you have a cheeseburger?" (cheeseburger, no) "No. Shoo, please." and back up he goes. At the vent: "Find
                 anything to eat down that duct?" (pie, heart) "He says there's a pie. He says it ain't his. He says that's
                 a technicality." (suit, eye, pie) "And a fella with a hoop round his neck, watchin' it like it owes him
                 money." "That's Jed. That boy's wanted a cheeseburger since five this mornin'." (suit, cheeseburger) "He
                 says the only thing Jed wants more'n that pie is a cheeseburger." "Then leave Jed to me, partner. I'm
                 gonna ask nicely."
              2. Grandpa Joe at the intercom (`intercomTree`): DISPATCH. PRESS TO TALK. As himself: "Houston, this is
                 Joe." "Mr. Grandpa, please return to your chair." ("Mr. Grandpa. Chair." "Mr. Grandpa, I have a building
                 to run.") "Ma'am, could I get a cheeseburger?" "Mr. Grandpa, you are not Jed." Honestly, on somebody
                 else's behalf: "Ma'am, I'm callin' on behalf of Jed. Jed would still like the cheeseburger." "...On behalf
                 of Jed." "Oh, for heaven's sake." On every speaker in the building: "Jed. Your cheeseburger is at the
                 front desk." And in the break room, for a moment: Jed up so fast the ice pack is still in the air.
                 "...Thank you, Houston." "Floyd. My cheeseburger, Floyd." Floyd, asleep: "...lunch rides in the back,
                 sir..." Jed goes. Houston: "That boy has waited since five this morning. ...Thank you for asking, Mr.
                 Grandpa." "Any time, ma'am."
              3. The pie. Ranger drops onto the fridge (pie, heart), along the counter, and eats Wendell's pie: the
                 nibble ("...!"), the whole pie (pie, heart), a pause, a satisfied lean back (heart, zzz). Then his best
                 bottle cap out of his stash, set in the middle of the empty tin (bottlecap, arrow, piepan): he does not
                 steal; he trades. The tin is sticky (piepan, water); he takes it, and the bottle cap stays on Wendell's
                 card (bottlecap, arrow, paper); at the sink he washes the tin the way he washes everything, and it comes up
                 shining (piepan, shiny). On the corkboard, the LAMPLIGHTER TEST SCHEDULE: he looks at it (lamp, clock,
                 joe) and takes it too.
              4. Back up through the vent over the fridge, along the duct, and down through ROOM C's grille to Grandpa
                 Joe: into his hands if he is on the chair, or onto the spare chair's seat ("That's twice this week
                 somethin's fell out of the sky on me."). The pie tin: "Well, look at that. Washed and shinin'." (piepan,
                 plus, banjo) "Round, and tin, and just the size. Great minds, partner." The schedule, read on the spot:
                 "What's this, partner? ...'LAMPLIGHTER. TEST SCHEDULE.'" "'30 OCT, 1747 HRS: SECTOR 1921. One civilian
                 vehicle, unconfirmed. See Form 7.'" "'31 OCT, 1700 HRS: SECTOR 44. B-7. Please do not look directly at
                 the sector.'" "Seventeen forty-seven. Yesterday, with the sun goin' low. That's when the sky opened over my
                 road." "One civilian vehicle. Unconfirmed. ...I can confirm it. Red, with wood on the sides." "They're
                 makin' 'em, Ranger. Every hole in my desert. They ain't findin' 'em." "They're MAKIN' 'em." (hole,
                 question) "Sector 44. Today, at five. ...Forty-four's the boy's year. Miss said so." "B-7. That's why they
                 need all that air. This little building goes DOWN."
Wrong tries:  Waking Floyd                   -> "...Regulation twenty-two, sir." (zzz) He does not wake.
              The vending machine            -> he presses every button. One packet of peanuts falls (peanuts, clock): for
                                                later. Again: nothing more comes. Handed down to Joe: "Peanuts. He's a
                                                planner."; and back up: "You keep them, partner. You're the planner."
              The pie with Jed there (from above) -> Jed is looking right at it
              The intercom before #18        -> no lever yet: Houston will not hear of a cheeseburger for Mr. Grandpa
              The pie tin or the schedule up the vent -> "I'll be needin' that one, partner."; "I'll hang on to this. It's
                                                the most important piece of paper in the building."
              Ranger at the intercom (if he drops into the room) -> "Dispatch." (cheeseburger, question) "...Mr. Grandpa,
                                                is there a raccoon on my intercom?" "Ma'am, I wouldn't want to say what
                                                ain't on the form."
Gives:        The pie tin (clean) and the schedule (`office.schedule`): the stage's revelation, and the reason to go down.
Plants/pays:  Pays off Jed's cheeseburger at last (ordered at 0500 in Act Four; delivered to the wrong man in the
              limousine; delivered to Jed now, on Grandpa Joe's word). Pays off Ranger's trades, and "Ranger's got the
              eyes for it". Plants Wendell's line in stage two ("Somebody ate my pie and left me a bottle cap. ...It is a
              very nice bottle cap."): the cap stays on his card.
Notes:        Grandpa Joe will not lie, and does not have to: the intercom's lever is offered once the banjo is back and
              Ranger has told him Jed is watching the pie. Ranger can also drop into the Comfortable Room once the suits
              have gone and Joe is off the chair, hop down, wash up at the cooler ("He's washin' up. Government water's good for
              somethin'."), and hand Joe the tin and the schedule himself; he climbs back the way he came ("Up you go,
              partner. Mind the... well. You ain't got a hat."). Hints follow the puzzle: Grandpa Joe, "A pie tin'd mend
              her. If there's a pie in this building, Ranger's the one'd sniff it out.", "Jed won't leave that pie for
              nothin' but a cheeseburger. And Houston's got the cheeseburgers.", "Jed's gone after his lunch. That pie's
              Ranger's business now.", "I'd bet that break room's got more in it than pie. Ranger's got the eyes for it.";
              Ranger (suit, cheeseburger, joe), (pie, piepan, joe), (piepan, water), (lamp, arrow, joe).
```

```
Puzzle #20: A Soundproof Room        (Act Five, continued · Lead: Grandpa Joe · the room, then the suits)
Needs:        #19
Setup:        Grandpa Joe has a broken banjo, a clean pie tin, and a reason to get to B-7 before five o'clock.
Steps:        The pie tin used on the banjo (the engine has no thing used on a thing in the pockets: the pie tin, or the
              banjo, used on anything in the room): "Hold still, darlin'. New head, comin' up." Bracket by bracket: "One
              bracket. Two. Three... and the rest. Snug." (`banjo-pie`, the pie-tin banjo) "Let's hear you, then." One
              string: the loudest sound the building has ever made. "...Oh, my. She's louder'n she ever was." And he plays.
              The ducts are quiet, every fan stopped, and sheet metal carries a tune like a trumpet: the Last Stop Rag goes
              through every vent on every floor. Houston: "Attention all personnel. There is... music. On the ground floor."
              The door: Dale and Merle in it, and Wendell behind them in the hall with his fingers in his ears ("Fella with a
              birthday button and his fingers in his ears. Happy birthday, son."). "Sir. PLEASE, sir." "Sir, it is in the
              ducts, sir. It is on every floor." "B-3 has called twice, sir." Then a talk (`ragTree`), and he plays on
              through it: "Can't stop, son. Medical condition." ("Sir, there is no medical condition in your file." "Son, at
              my age I am a medical condition." "...I will add it to the file, sir. Sorry, sir."); "This here's the Last
              Stop Rag. Y'all want to hear it twice?" ("No, sir. Sorry, sir." "Once was very nice, sir." "Sir. Please. It is
              my birthday."); and, once the schedule is read, "Lamplighter." ("...Sir. Where did you hear that word, sir?"
              "A raccoon brought it to me, son." "Sorry, sir. That is a green-page word. It is on B-7." "MERLE." "...Sorry,
              Dale.") and the lever: "Y'all got somewhere I can play where I won't bother nobody?" "Sir, the only
              soundproof room in the building is B-7." "We are not authorized to take civilians to B-7, sir." He plays
              louder. Wendell: "Dale, it is my BIRTHDAY." "...Sir, we are now authorized."
Wrong tries:  Playing the broken banjo       -> one dull clunk: "That ain't music. That's furniture."
              Playing before the schedule    -> the suits come, beg, and he stops when asked nicely: "Well. Since y'all
                                                asked nice." "Thank you, sir." "It is a very nice song, sir. Sorry, sir." "For
                                                your comfort, sir." They lock the door again, and nothing changes: he does
                                                not yet know where he wants to go. Played again, Houston: "B-3 would like the
                                                music to stop. So would B-4. So would I."
              Asking to go home              -> "Sir, you have not completed the questionnaire."
Gives:        Grandpa Joe on his way down (`office.down`), and Going Down.
Plants/pays:  Pays off the singing in the limousine (the suits will do anything to make it stop: they will even take him
              where he wants to go). Pays off the stopped fans (#16): Ranger can go down the B-7 shaft.
Notes:        Hints: Grandpa Joe, "A broken banjo and a clean pie tin. Jolene'd say that's a banjo waitin' to happen."; once
              mended and nowhere yet to play to, "I could play 'em right out of this room. I just don't know where I'm playin'
              to yet."; once he knows, "Them boys'll do anything to make the Rag stop. Even take a man where he wants to
              go."; Ranger (joe, music), and where Joe hears him, "He says play it, Joe. I aim to, partner."
```

```
Cut-Scene: Going Down        (ends the stage, and the demo)
```
A title, "Going Down". Then the Comfortable Room through the slats of ROOM C's grille, Ranger's eyes in the vent: Grandpa
Joe walks out across the room playing the pie-tin banjo, hat on, between Dale and Merle, and Wendell already out in the
hall with his fingers in his ears. "Y'all ever been down to B-7?" "No, sir. We have never been authorized, sir." "Well. Now
you are." "It is still my birthday, Dale." "Noted, Wendell." Out through the door, one after another. Houston, on every
speaker: "Attention all personnel. The music is going down to B-7. Thank you for your patience." Then Ranger along the
duct, lying at the grille over the HALL, and the elevator heard through the slats under him: its own polite little tune,
and "Turn that off, son. I brought my own." "Mind the--" "Minding the hat, sir." The doors close on the Rag (joe, down).
Ranger goes on to the end of the duct, to the B-7 shaft, its big fan stopped; he looks down it (down, joe, heart), sits up
and looks at us in his mirror shades ("...!"), and hops down the shaft after him. Houston, to nobody in particular:
"Lamplighter test at seventeen hundred hours. Sector 44. Please do not look directly at the sector." The card:
LAMPLIGHTER, and smaller, "to be continued". Then `office.done` (the gate, `office.end`), `demo.done`, and the title
screen. Skipped, the same; the card is after the part that can be skipped, so it always shows.

---

## Ledger for this chapter

**Things that are carried**

| Thing | Comes from | Who can hold it | Used for |
| --- | --- | --- | --- |
| Study key | Inside the piano, Act Three #2. Only Little Sister can get it out. | Little Sister; then whoever she gives it to | Act Three #3: whoever holds it opens Dad's study |
| Little Sister's flashlight | Her blanket fort, in her room. Only she may take it. It is dead. | Little Sister (it can be lent, and must come back) | Act Three #4: it wants batteries. #5: the dark of the closet under the stairs |
| Batteries | Big Sister's sound machine, in the Retreat, Act Three #4. Only she may take them. | Big Sister; then whoever she gives them to | Act Three #4: handed to whoever holds the flashlight (or the other way about), they go into it, and are not seen again |
| Sticky note | The monitor in the study, Act Three | Any of the three | Act Three #6: only Big Sister can read what it means |
| Dad's pencil | His crossword, on the arm of his chair in the living room | Any of the three | Act Three #8: Mom winds the answering machine's tape with it |
| Spare car key | The family vault, Act Three #10 | Mom; then whoever she gives it to | Act Three #11: they cannot leave without it. Mom drives. |
| Silver coin | The Son takes it from a fountain in Rome, opens a door the size of it with the morning sun, and tosses it through (Act Two). It hits Grandpa Joe's hat in Nevada, and Ranger has it before it stops ringing. <!-- NEVADA-12W --> | The Son; then Ranger; then Big Sister, by trade (#10), and whoever she gives it to | Act Four #6: only Big Sister knows what it is. Act Four #9: any of them can flash the sun off it. #13: it goes through the door with them |
| Four pennies <!-- NEVADA-12W: the rows to the next comment are round twelve's --> | The take-a-penny dish in the store (#10, a wrong try): one is the lucky `penny`, three are `pennies` | Little Sister. The lucky one she may hand to anybody; the three she will not ("No! They're MINE. I took them FAIR. It SAID.": handed over, they come straight back) | The lucky penny goes through the coin door to her brother, for luck (the letterbox: whoever holds it, Little Sister posts it); it waits in the tunnel for the Rome end. Ranger does not want copper. |
| Mirror shades | The spinner rack; Mom buys them ($3.99) | Any of the three | #10: traded to Ranger by Big Sister. He wears them from then on. |
| One warm egg | Darlene, out back (#11) | Little Sister ("It's WARM. It's MINE to keep warm.") | Not yet. The one thing in her pocket that must be kept warm, wherever they land. |
| Three waters | The survival shelf; Mom buys them | Mom | Not yet. "We are going somewhere with no shops." |
| The sun shade | The front window, DISPLAY ONLY. After #11 Jolene lifts it out and gives it to whoever asks for it (#12) | Any of the three, then Grandpa Joe | #12: held in the low sun by Grandpa Joe; the door as wide as a windshield. It stays with him. |
| The map of the sectors | Jed's clipboard, in the limousine (Act Five #15) | Grandpa Joe (Ranger puts it in his bib pocket) | Not yet: three sectors, one of them under Jed's thumb, and a blank column headed WHAT OPENS THEM. <!-- SCENES-17 -->It stays in the bib pocket through the Office: "Not the map, partner. That map's comin' home with us." |
| The receipt for the banjo | The backup, through the divider (Act Five #15) | Grandpa Joe <!-- SCENES-17 -->(then Ranger, up through the vent) | Not yet. It reads "RECEIVED: one banjo (damaged). one raccoon (unconfirmed)." <!-- NEVADA-12W: end of round twelve's rows --> <!-- SCENES-17 -->The Office #18: down through PROP & EFF's grille to Opal, claim number 3117; the banjo is returned on it. |
| Banjo (damaged) <!-- SCENES-17: the rows to the next comment are round seventeen's --> | Property & Effects, tag No. 3117: the banjo Jed's head went through. Opal returns it on the receipt (the Office #18) | Grandpa Joe ("She won't go through there, partner.") | The Office #20: mended with the pie tin. Played broken, "That ain't music. That's furniture." |
| Pie tin | Wendell's pie, in the break room (#19): Ranger eats the pie, leaves his best bottle cap, and washes the tin at the sink till it shines | Ranger; then Grandpa Joe (down through the vent, or by hand in the room) | #20: the banjo's new head |
| Pie-tin banjo | The banjo (damaged) and the pie tin, put together by Grandpa Joe (#20) | Grandpa Joe | #20: the Last Stop Rag through every vent in the building, until the suits take him where he won't bother nobody: B-7 |
| The test schedule | The break room's corkboard (#19): LAMPLIGHTER. TEST SCHEDULE. | Ranger; then Grandpa Joe, who reads it at once ("I'll hang on to this.") | The stage's revelation (`office.schedule`): 30 OCT, 1747 HRS, SECTOR 1921; 31 OCT, 1700 HRS, SECTOR 44, B-7 |
| Bottle cap | Ranger's stash, his best, from the arrival on | Ranger ("He says that's his best one, and it ain't for givin'.") | #19: traded for Wendell's pie; it stays on Wendell's card |
| Packet of peanuts | The break room's vending machine: every button (#19, a wrong try) | Ranger; Grandpa Joe hands it back ("You keep them, partner. You're the planner.") | Not yet. For later. <!-- SCENES-17: end of round seventeen's rows --> |

The five things from the house that are not used up (the key, the flashlight, the note, the pencil, the car key) are still in their pockets in Nevada. The batteries are in the flashlight.

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| "Daddy's not lost. Daddy's EARLY." | Opening of Act Three | "Some when", in the middle of Act Four |
| Dad never asks for directions | The voicemail; Little Sister's postscript to the prayer ("please make Daddy ask for directions. Just ONE time."); the wedding photograph on the landing | Act Three #7, the wedding question. (Draft: the last thing Dad does in the game is ask for directions. That would also be a seven-year-old's prayer answered.) |
| "THE MANAGEMENT" | Act Three #1, Dad's notice | Act Three #10: the vault's label ("Your mother will know. She brings it up.") and the card inside it ("KNEW YOU'D KNOW.") |
| "I FIT!" | Act Three #2 (under the keyboard) and #5 (the closet) | The fence: "I could fit under that. I fit under EVERYTHING." For the next act. And the coin-sized door: "I bet I could still FIT." |
| Handing a thing to someone | Act Three #3 (the key), #6 (the note), #8 (the pencil) | Act Four: the mirror shades, from Mom to Big Sister (#10); the coin, handed round before #9 so that any of the three can flash it; the sun shade, to Grandpa Joe (#12) |
| The road sign that changed its mind | The intro | Act Three #9: "That sign just changed its--". Then Grandpa Joe's account, Act Four #5 |
| 5:41 on the tape; 5:47 on the map | Act Three #9 and #7 | Whichever comes second: Big Sister counts the six minutes |
| "Thirty-seven miles past Last Gas" | Act Three #7 (the map) and #9 (Dad says it himself) | The first line of Act Four |
| The ketchup packets Dad is saving | Act One (his running gag) | Act Three #10: two of them are in the family vault. Nobody has asked what he is saving them for. |
| "I still want a dog" | Rome, Act Two: "Edge, we get a dog." | Act Three: it is the password on his bedroom door. Little Sister does his voice, it is CORRECT, and his booby trap goes off anyway. Not yet answered. |
| NO GIRLS ALLOWED, and eight foam darts on the runner | Act Three, the Son's door: "I don't want to go in there. The rug is probably booby-trapped." | Not yet. He will want a full report (Big Sister intends to say it was adequate); Mom has left the darts where they fell, for him to count. |
| "NO BROTHERS. Except on Saturdays." | Act Three, Little Sister, when the trap gets her sister | Not yet: the sign is not made. |
| Her loose tooth, "not allowed out till Daddy's home. He has to SEE it." | Act Three, a word with Big Sister in the study | Not yet. |
| Psalm 121:8: "thy going out and thy coming in" | Act Three #11, at the front door. Mom: "Going out, and coming in. All five of us." | Act Four #13: said again, at the door (below). Not yet: the coming in. (Mom's "My times are in thy hand", Psalm 31:15, is the second line after "Daddy's EARLY", in "Some when".) |
| Little Sister's flashlight | Act Three #4 and #5 | Act Four: light opens doors in this story, and hers is too small to be seen in the morning sun. For later. |
| "Chickens KNOW." | Act Three, Little Sister at her flock | The geese in Egypt, the sacred chickens in Rome, Grandma Jolene's hens in Act Four (#5: they quit laying the day the sky opened and stand facing the fence; Little Sister: "That's EVIDENCE. Chickens KNOW."; and #11): in every era the birds face a door in time before any person has noticed it. |
| General Feathers' place on the pillow: RESERVED | Act Three, Little Sister's room | She is in Dad's suitcase in Egypt (Act One), in charge. In Act Four, once she has heard of Grandma Jolene's hens, Little Sister misses her: "Mommy, I miss General Feathers. But Daddy needs her MORE. She's keeping an eye on him. He has to do what she SAYS." "Then he's well looked after, sweetheart. She outranks him." Not yet: her coming home. |
| 1921 B.C. and 44 B.C. on Big Sister's timeline | Act Three, the Retreat | The two sectors on the notice in Act Four. In "Some when": "Sector 1921: nineteen twenty-one B.C. It is on my timeline: the year Abram went down into Egypt." |
| "The Retreat goes dark so that the internet may live." "I intend to mention this again." | Act Three #4 | Not yet. She will. |
| The appeal lodged against rule three (NO CHICKENS) | Act Three, the rules in the Retreat | Not yet heard. |
| The coin that "didn't come back down" | Rome, Act Two | #5 and #6 |
| "Sun was low. Hit the chrome on that wagon and threw a flash up ahead, like a signal mirror." | #5, Grandpa Joe's account | #9: the coin, held up to the low morning sun; #12: the banjo, and then the sun shade |
| "Look at the edges. It is NEW." | #6 | #9: a new coin shines |
| "Why is the sky DOWN?" | Rome, Act Two, looking through the coin-sized door | #5: the coin fell out of the sky and hit his hat |
| A Geiger counter that never clicks | #5, ask again as Mom or as Big Sister | Not yet. The radiation is an excuse: for what? |
| Sectors 44 and 1921 | #8 | Act Five #15: the office's own map has them, and a third, under Jed's thumb. Not yet: who numbered them, and how many more there are. |
| A hum where there is nothing to hum | #9, before the coin goes up | #9. It is the door, shut. |
| A door the size of a coin, with a morning in it | "Some when" | The letterbox: the Son is on the other side of it. #12: more light, a bigger door (nobody told them). #13: they walk through it. |
| Sausages | "Some when": the second thing Little Sister notices (the first is chickens) | The letterbox, if the player has him tell it: "It smells like sausages out here." Her brother found Rome's snack bar the same way: "Step one, I can SMELL you." |
| "Father, You know where they are tonight, and I do not. Keep them." "And bring us to them." | Act Three, the opening prayer | Act Four #9, before the coin goes up: "Father, You brought us this far. We don't understand what comes next. You do. Keep us, and keep them. In Jesus' name." |
| Little Sister's postscript to a prayer | Act Three: "And please make Daddy ask for directions. Just ONE time. Amen." | Act Four #9: "And thank You for the lemonade. And tell Daddy we're COMING, so he doesn't have to be brave by himself. Amen." Not yet answered, either of them. |
| "Places, girls." | Act Three, the opening (and the title of Big Sister's next chapter) | Act Four #9: Mom says it, and the three take their marks at the glass; #13: "Places, girls. Hold hands. All the way through." |
| George Washington's 110 Rules of Civility | Act Three, a word on the landing | Act Four #7: Mom's second try at the man in gray. "I can neither confirm nor deny General Washington." |
| "Is Daddy in trouble?" | Act Three, a word in the study | Act Four, a word with her mother: "Mommy, is Daddy STILL in trouble?" "A little, sweetheart. But only with me, and only once he's home." |
| The tribute money, in a ten-year-old's own words | Rome, Act Two, at the fountain: "So Caesar gets his coin. And God gets what's God's." | Act Four #6: the same coin, and his mother has the verse (Matthew 22:21) |
| "That is not what early means." | Opening of Act Three (Big Sister) | "Some when", in Act Four: "Wait! What's B.C.? Somebody tell me QUICK." "Before Christ, sweetheart." And then it is exactly what early means. |
| Little Sister's loose tooth: not allowed out till Daddy has seen it | Act Three (a word with her sister in the study) | Act Four: it is not for sale ("It's waiting for Daddy"), and when they find him it comes second, after the internet. Not yet: Daddy sees it. |
| "I'm not scared. I'm BRAVE-scared." | Act Three #5, the closet | Act Four, holding her sister's hand by the fence: "Okay. I'm holding it MIGHTILY. I'm not scared. I'm BRAVE-scared." |
| "Chickens KNOW." <!-- NEVADA-12W: the rows to the next comment are round twelve's --> | Act Three; Act Four #5 | #11: Jolene's hens are guarding, not waiting; Little Sister is the only one they will listen to. The cut-scene: five hens turn to watch the limousine go. |
| General Feathers, keeping an eye on Daddy | Act Three, the RESERVED pillow; Act Four | #11: "That's what General Feathers is doing for Daddy." |
| "I FIT!" / "I bet I could still FIT." | Act Three; "Some when" | Her head in the hole ("there's a chicken LOOKING at me"); the banjo-sized door ("I could fit SIDEWAYS." "No."). Not yet: a door her size that she goes through. |
| The old man's flash: "like a signal mirror" | #5 | #12: the sun shade, "a mirror the size of a windshield" |
| Dad's windshield shade (Act One) | Egypt | #12: his family opens their door with a windshield shade; Mom's "I said it was for show." "...Then it was for this." |
| "Do you get a snack?" | #7 | Jed: "I have not had a snack since 0500."; "I need a cheeseburger and backup"; "Who ordered a cheese burger?"; Act Five #15: Grandpa Joe eats it. |
| "Hi, Mister Gray's mommy!" | #7 | Houston: "Jed, is that the child again?"; "Houston, we have a problem" is her name. |
| "That's what the gray suits drive." | #5 | The limousine. |
| The banjo flashes in the sun | The porch, when he plays ("Can you play your banjo? PLEASE?") | #12's half-answer: a banjo-sized door. Then the cut-scene: it is a weapon, once. |
| "I been holdin' things for Jolene since 1974." | #12 | The cut-scene: he lets the light down, the door shuts, and the backup have nothing to see. Not yet: he and Jolene keep the door. |
| Psalm 121:8, "thy going out and thy coming in" | Act Three #11 (the front door) | #13: Grandpa Joe has it from a plate in the kitchen, and says it to "coming in"; Mom finishes it. The coming in is still to come. |
| "Nobody holds this banjo but me and the Lord." | #12 | The cut-scene: what is left of it is evidence ("The banjo is evidence, sir. You will receive a receipt."); Act Five #15: the receipt. |
| Ranger trades, and does not like grabbers | #5, #10 | Act Five #14: the bow is a trade like any other; #15: the pickle, and the map ("That ain't stealin'. That's tradin'."). |
| "Is that YOU?" "I asked FIRST." "I asked EARLIER." | The letterbox | Not yet. |
| "Dad went through his door to come to me. He didn't come. Mom. Don't go through yours." | The letterbox | #13: they go through anyway, together ("Your father went through alone. We shall go through together."). Not yet: where Dad is. |
| The lucky penny in the tunnel | The letterbox | Not yet: it comes out at the Rome end. |
| "Jolene! Don't sell my rocks!" "I'll sell every one of 'em, Joe!" | The cut-scene | Not yet: she does not sell one. |
| The hens turn to watch the limousine | The cut-scene | Not yet: chickens know where Grandpa Joe is, too. |
| "They figured it out." | The cut-scene (Jed) | Act Five #15: the office's column WHAT OPENS THEM is blank. The family knows; the office does not. |
| The third sector, under Jed's thumb | Act Five #15 | Not yet: the story's next door. <!-- NEVADA-12W: end of round twelve's rows --> |
| Mom is humming "O God, Our Help in Ages Past" | Act Four, a word with Little Sister | Not yet, and never said aloud: it is the hymn made from Psalm 90, which is the psalm Dad says at the door in Egypt (Act One). To confirm before anyone leans on it: see "To confirm", at the end of this document. |
| Grandma Jolene's hens, facing the fence | #5, his account: "Been a strange week. Jolene's hens quit layin' the day the sky opened. Stand out back all day now, facin' that fence." | "Some when": through the door, it is Little Sister who hears chickens, before anybody smells a sausage. #11: they are guarding. |
| "The holes open on years that MATTER. ...I don't know why." | "Some when" (Big Sister): the Ides of March, and Abram in Egypt | Not yet. Nobody explains it. (It is also the first time she says "I don't know" in this act.) |
| "I never once thought of it as an ordinary morning." | "Some when" (Mom, of Genesis 12) | Not yet. Her husband is standing in that chapter. |
| Jed's cheeseburger <!-- SCENES-17: the rows to the next comment are round seventeen's --> | Act Four #7 ("since 0500"); Act Five #15 (eaten by the wrong man) | The Office #19: asked for on Jed's behalf, and sent to the front desk at last. "...Thank you, Houston." |
| The singing: the suits will do anything to make it stop | Act Five #14 | The Office #20: they will even take him where he wants to go, and that is B-7. |
| The receipt's "one raccoon (unconfirmed)" | Act Five #15 | The Office #18: Opal looks up at the vent. "...Confirmed." THUNK. |
| Lamplighter | The Office #17: the green page, which they are not supposed to read | #19: the test schedule; #20: "That is a green-page word. It is on B-7."; the last card. Not yet: what it is (stage two). |
| "Seventeen forty-seven. That's an awful particular minute, son." | The Office #17 | #19: the schedule: the minute the sky opened over his road. "One civilian vehicle. Unconfirmed. ...I can confirm it. Red, with wood on the sides." |
| Sector 44, the boy's year | Act Four #8 (the notice) | The Office #19: the next test, today at five. Not yet: what happens at five (stage two). |
| The building's air, turned off by a raccoon | The Office #16 | The heat (#17); Going Down: the B-7 shaft's fan is stopped, and Ranger goes down it after him. |
| Ranger's best bottle cap | The Office's arrival (his stash) | #19: traded for Wendell's pie, and left on Wendell's card. Not yet: "Somebody ate my pie and left me a bottle cap. ...It is a very nice bottle cap." (stage two) |
| Opal's keys, and the Director's Roman sandal (1951) | The Office #18 | Not yet (stage two). |
| Grandpa Joe never lies | The Office #17: every answer true, on every path through the questionnaire | #19: he asks for Jed's cheeseburger on Jed's behalf, and it is true. <!-- SCENES-17: end of round seventeen's rows --> |

(The last rows are Act Four's and Act Five's, and their puzzle numbers are those acts' own; <!-- SCENES-17 -->the
Office's, the last ten, are Act Five's too, #16 to #20.)

**Facts used.** In Act Three the riddle (#1: a piano's eighty-eight keys), the password
(#6: sliced bread, 1928), the tape (#8: a cassette can be wound with a pencil) and the
vault (#10: the Constitution signed in 1787, the Declaration adopted in 1776, the new
government and Washington's oath in 1789) rest on real history; so do the things Mom
and Big Sister say for the pleasure of it (Luther's hymn, Abigail Adams's letter,
Washington's Rules of Civility, Adams and Jefferson, Bach's "S.D.G.", Cristofori's
piano, what B.C. and A.D. mean, the year Archbishop Ussher's book was published). The
years before Christ on Big Sister's timeline (4004, 2348, 1921, 1491) are the Bible's
count, as Ussher counted it: the author's rule for the whole game. Six verses of
Scripture are quoted in Act Three, and nine words of a seventh (Matthew 23:37), and two in
Act Four (Matthew 22:21 at the coin, and the first clause of Psalm 31:15 in "Some when"), from
the King James Version, each listed with its reference (since round seventeen a reference is
said aloud only where it is natural: in Act Three, by Big Sister). In Act Four the bomb tests (#8), the coin
(#6) and 44 B.C. ("Some when") rest on real history, and so do the things Mom and
Big Sister say for the pleasure of it (Reformation Day, the coin of the tribute money,
General Washington's rules, "In God We Trust" and the year 1864, Dr. Franklin's rising
sun, what B.C. means). The other year, 1921 B.C., the year Abram went down into Egypt
(Genesis 12:10, told and not quoted), is the Bible's count, as on Big Sister's timeline.
The lists, and which of them have been checked against a source, are at the end of
[CHARACTERS.md](CHARACTERS.md): Big Sister's facts, Mom's facts, and the verses. One of
Act Four's was reworded on 2026-10-07 to say less and be surer: of the coin, only that
in 44 B.C. coins were struck in Rome with Caesar's own portrait while he was alive (not
that he was the first). The second sector on the notice was the textbook's year for the
Great Pyramid until the evening of that day; it is now 1921 B.C., the Bible's count,
stated as plain fact, and nobody in the act speaks of the pyramid.
One of Act Three's was reworded the same day on the fact-checker's finding: a cassette
is wound with "a pencil", and nobody says that the pencil's six sides are why it fits.
<!-- NEVADA-12W --> Round twelve added these, each checked against a source: no bird alive has
teeth; raccoons have no pocket, and the Virginia opossum's mothers have a pouch; a hen takes
about a day to make one egg; a rooster never lays one; a hen lays less when she is frightened;
the raccoon's Latin name, and that "lotor" means "washer"; a raccoon's most important sense is
touch, and water is thought to make his front paws feel more; and Mom's "A matter of record:
Nevada is the driest state in the Union." Grandma Jolene's four facts are wrong on purpose, and
each is put right by Big Sister. Psalm 121:8 is said again, King James Version, split between
Grandpa Joe and Mom. The sources are in [CHARACTERS.md](CHARACTERS.md), in the tables.
<!-- SCENES-17 -->The Office (round seventeen) states no history of its own and quotes no Scripture: Grandpa Joe's prayer
when the suits have gone is his own words ("Lord, You know where that family is, and I don't. You look after 'em."), and
"before church" is in his first line there. Its years are the story's (1951, 1971, Sectors 1921 and 44).

**How it was checked.** Act Three: `briefs/out/check-home.mjs` reads the act's five
scene files, its lines, its beats, the carried things and the sounds against each
other and against the painters' measurements (walk outlines, places to stand, cut-outs;
and that every place to stand can be walked to from every way in), and plays the act
two ways on a stand-in for the engine, trying everything as each of the three before
every step. `briefs/out/play-home.py` plays it two ways in the
real game by real clicks, by different orders of the middle chains, and keeps a picture
of every scene and every moment worth looking at in `briefs/out/home-shots/`. Act Four:
`briefs/out/nevada-check.mjs` reads the act's files against each
other, against the painter's measurements and against the author's instructions, and
plays it three ways on a stand-in for the engine. It holds the two verses letter for
letter against the fact-checker's list (`briefs/out/facts-home.json`), keeps a table of
every line that states history with where it was checked, sees that every year before
Christ is the Bible's count and every span of years the right sum, keeps the oldest
history to the reveal and the chickens to three to six lines (Little Sister hearing them
first), and sees that all three stand in prayer while the prayer is said and nobody after
it. Since round three it also holds Little Sister's two kept lines word for word, sees
that she says "Mommy" and "Daddy", that "radiator" is her one word that comes out nearly
right, and that she counts the man in gray's questions right; that every area hugs its
thing (no rectangles), that cut-outs and people are named for Show, that no area lies over
the places where the three of them stand to be talked to, and that the scene has no ways
out at its edges. `briefs/out/nevada-play.py` plays it three ways in the real game by real
clicks, with a different one of the three holding the coin at the end each time, the first
two times with things from the house in their pockets, and keeps a picture of every moment
worth looking at in `briefs/out/nevada-shots/`; it hears every one of Little Sister's new
lines, turns Show on for a picture before and after the man in gray moves (every thing
outlined, the cut-outs, the people and the three of them by their own pictures, and no
arrow), and clicks in a band along the edge to see that nobody leaves. <!-- NEVADA-12W --> Round
twelve: the talks (`js/content/talk/nevada.js`) are tested by the writer's `trees-check.mjs`:
every node and line they name exists, every option is said by the one who picks it, and a
stand-in for the engine plays each tree as the engine's own `talk()` does, by walkthroughs that
reach every fact the act needs and by random walks from every state. Each of the three parts
was built with a play of its own, in the real game by real clicks, and each was run again on the
merged game: `play-roadside.py`, three ways from the arrival to the walk through (a different one
of the three holding the coin at the end each time; all 508 of the roadside's lines are said);
`play-store.py`, two ways (everything looked at and tried as each of the three, and out and in
again for every one of Jolene's hats; and the quickest way through #11; all 246 of the store's
lines are said); and `play-limo.py`, two ways (the cut-scene watched, and Act Five the long way
round to the card and the title; the cut-scene skipped, and Act Five the short way; all 148 lines
of the cut-scene and Act Five are said). The store's play and the limousine's end NO PROBLEMS.
The roadside's play stood in for the store and the cut-scene while those were being built, and on
the merged game its checks of what comes after the walk through still expect the stand-in: that
is all it reports. `nevada-check.mjs` and `nevada-play.py` are the old act's: they are to be
rewritten for the act as it is now (one play through the whole act and Act Five, with the three
part plays beside it), and the testers' checkpoints made again from them.
<!-- SCENES-17 -->**The Office (round seventeen).** `briefs/out/office-check.mjs` reads the stage's files against each
other and against the painters' layouts (every mark on a floor, every shape inside the picture, every picture on disk,
every painted thing clickable but the painters' extras, which have no lines; the ducts' shapes the painter's, by
`office-ducts-shapes.py`), the map, and the lines of the limousine and Act Four as they were at the start of the round;
it sees every line of `office.en.js` said by something, every thought's pictures drawn, no Scripture reference and no
real song said aloud; walks every tree at random as the engine does; and plays the stage's own scripts on a stand-in for
the engine, from the arrival to the title, and every area of every scene tried by each of the two who can be there, in
five moments of the story and from above. `briefs/out/play-office.py` plays the stage two ways in the real game by real
clicks, from the limousine's end (the arrival watched, and skipped), every puzzle, every wrong try and hint of the design,
every grille looked through, dropped through and climbed back, things handed up and down, a save and a load in the middle
of each puzzle, the ending and its card; it keeps a picture of every moment in `briefs/out/shots-office/`. The Office's
talks are walked by their writer's trees check (WRITE-17's `tools/trees-check.mjs`). `nevada-play.py` and `play-limo.py`
go on into the arrival now, and `nevada-check.mjs` expects the demo's end at Going Down. `briefs/out/map-sweep.py` sweeps
the Office's map at each of the stage's checkpoints: the way between the lot and the ducts there and back, Grandpa Joe
refused in his own words, B-7 in each one's, the rooms Ranger reaches by the grilles shown by name only, and the
portraits.

## What comes next (not written)

<!-- NEVADA-12W: round twelve answered three of these (how they follow: #12 and #13; what the man in gray does
when he turns round: the cut-scene "Backup"; when the two halves first hear from each other: the letterbox). -->
- Where the family comes out (decision 1: the next stage's). They walked into a door
  that opened on a Roman morning; the Son warned them that Dad went through his door
  to come to him and did not come.
- What the Office Of Peculiar Sectors does with Grandpa Joe, his map and his receipt,
  at the gate of a very small building with a very long name (Act Five, after #15).
  <!-- SCENES-17 -->Answered in round seventeen: the Office's stage one, above. Next, stage two, "Lamplighter"
  (`briefs/out/office-hq-design.md`, section 5): B-7, Dr. Fairweather and her lamp, the five o'clock test on Sector 44,
  and Wendell's very nice bottle cap.
- The penny in the tunnel, which comes out at the Rome end; the egg, which must be kept
  warm; the third sector, under Jed's thumb.
- Why the doors open on years that matter (the Ides of March; Abram in Egypt). Big Sister
  has noticed, and does not know why. Nobody explains it yet.
- What the men in gray know, and whether they are after the same thing.
- Little Sister eyed the fence: "I could fit under that." Still for later.

**To confirm** (wording and facts in Act Four)

- The hymn's title (`nevada.talk.lilsis.mom.3b`), written from knowledge and not from the
  fact-checker's list: "O God, Our Help in Ages Past" (Isaac Watts, 1719). Watts's own first
  line is "Our God, our help in ages past", and some hymnals give the title so. Which does
  the author's hymnal print? Only the title is in the game.
- That the hymn is Watts's paraphrase of Psalm 90, the psalm Dad says at the door in Egypt
  (`egypt.gate.psalm.1`, Psalm 90:4). Neither act says so; if one ever does, check it first.
- "Reformation Day" as the name of 31 October (`nevada.arrive.2b`). The date of the
  Ninety-five Theses was checked; the name of the day was not an item of its own.
- "Ours says 'In God We Trust.'" (`nevada.talk.mom.bigsis.quarter.a`). What was checked is
  that the motto was first on a United States coin in 1864, and is the national motto
  (1956). That it is on the coins in a handbag today is taken as common knowledge.
- "Before Jesus was born" (`nevada.gate.2d`): Mom's gloss of "before Christ" for a
  seven-year-old, and what the count means. Historians put the birth itself a few years
  before A.D. 1; nothing in the line depends on that.
- The years. Every line that gave the textbook's year for the pyramid, or leaned on it, has changed (`nevada.notice.mom.1`,
  `nevada.notice.big.2`, `nevada.notice.again`, `nevada.gate.2b`, `nevada.gate.5`). Big
  Sister's "it isn't two thousand years old" (`nevada.coin.read.3`) is about 44 B.C., and
  stands: a coin of 44 B.C. would be 2,069 years old.
- "What's B.C.?" (`nevada.gate.2c`) is asked although Big Sister's timeline at home explains
  B.C. the night before (`home.timeline.bigsis`). A seven-year-old asking twice is in
  character; if the author would rather she remembered, `.2c` and `.2d` can go, or be
  turned round so that she answers it herself. Nothing else depends on them.
- The hens are heard of, not heard: nothing is drawn, and the game has no chicken sound. If
  one is wanted from behind the shack, it belongs in `js/content/sound.js`. (Round twelve:
  they are drawn now, in the hen yard behind the store, and still make no sound.)
- <!-- NEVADA-12W --> Big Sister's "No, thank you. Non, merci. Nein, danke."
  (`nevada.store.eggs.bigsis`): French and German, written from knowledge.
- The goodbye with Jolene (#13). The design had Big Sister say "A hen cannot count to five"
  and Jolene answer "She can if she's counting eggs, sugar." That fact is not used (chicks
  have been shown to tell small numbers apart, so Jolene might be right by accident), and
  the goodbye is about the egg instead. If the author wants the design's, the fact must
  change too.
- Houston. Little Sister calls the voice in Jed's earpiece "Mister Gray's mommy"; the
  design names her Houston Pruitt, dispatch, thirty-one years of service. Nobody in the
  game says "Pruitt" or her years yet, and she has one line.
- Mom's car is painted teal, and her lines now say so ("a sensible teal sedan"); her third
  guess at Dad's car is "A gray car with dark windows." (DESIGN.md, section 14, item 17).
- Ranger sits on the ground beside the rocking chair, and Mom's look at him now says so
  (DESIGN.md, section 14, item 16).
