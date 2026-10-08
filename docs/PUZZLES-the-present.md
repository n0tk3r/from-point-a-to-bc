# The present: puzzle document

The part of the game that starts in the present, with the rest of the family: Mom,
Big Sister (13) and Little Sister (7). At home, that evening, they pray, go through the
house, and find out where Dad's phone was last seen and what he last said. Then they
drive to the middle of the Nevada desert, find a witness, learn that the government
has been closing parts of the desert for "elevated radiation", and open a door in
time exactly the size of a coin.

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
writer's, and is being brought into step with the new years (the notice now seals
sectors 44 and 1921).

Play it: `index.html?scene=home-living-room` starts Act Three and
`index.html?scene=nevada-roadside` starts Act Four. In the full game it follows Rome,
on a card that reads "Meanwhile, about two thousand years later". The other four rooms
of the house open the same way, with the facts that get you there:
`?scene=home-landing&lead=bigsis&flags=home.arrived`,
`?scene=home-study&lead=mom&flags=home.arrived,home.keyInPiano,home.hasKey,home.studyOpen`,
`?scene=home-lilsis-room&lead=lilsis&flags=home.arrived`,
`?scene=home-bigsis-room&lead=bigsis&flags=home.arrived,home.flashTaken`.

Puzzles are numbered within each act for now: Act Three's are #1 to #11. Act Four's
still carry the numbers they had when Act Three had four puzzles (#5 to #9), and want
renumbering when that act's revision is merged. Where the ledger at the end names a
puzzle, it says which act. When the whole game has a puzzle document they take their
place in one run of numbers.

## The idea of the chapter

Dad and the Son solve puzzles across time. Mom and the girls solve them **across each
other**: three people in one place, and every puzzle needs the right one.

| | What only she can do | In Act Three | In Act Four |
| --- | --- | --- | --- |
| **Mom** | Adults listen to her, and she knows her husband, her piano and her country | Sees the key in her piano; answers the question about the wedding; winds the tape; knows the year the vault wants | Gets the witness to talk; knows the car |
| **Big Sister** | Remembers the fact | Reads the riddle (eighty-eight keys); hears which note the key is under; knows the year behind the password; and it is her sound machine, so only she may take its batteries | Knows the coin, and reads the notice for what it means |
| **Little Sister** | Fits in small places and can distract anybody | Gets under the keyboard and into the closet under the stairs; owns the flashlight, and the fort it lives in; knows her brother's password, and chickens | Asks the man in gray two hundred questions |

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
- LITTLE SISTER: seven, small but mighty; has started before you have finished explaining; adds her own postscript to a prayer; wants to help, right now. Loves chickens above everything. Her favorite, General Feathers, went on the trip in Daddy's suitcase, to keep an eye on him.
- DAD (a voice on the voicemail, and on his own answering machine): is either driving or lost, and is never lost. Signs his notices "THE MANAGEMENT".
- THE SON (a voice on the toy alarm on his bedroom door): "Operation Keep Out." He still wants a dog.

The family are Reformed Christians, and it shows the way music shows in this house:
grace is said, the Bible by Dad's plate is read after supper, the children know their
verses, and when Dad does not come home the first thing Mom does is pray. How that is
written (King James only, exact and brief, with its reference; hymns named, never
quoted; nobody preaches) is in [CHARACTERS.md](CHARACTERS.md).

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
|  stairs      (toy alarm;     photos  DOOR (BEWARE     LADDER     table    STUDY  |
|  window      shut all act)           OF CHICKENS)     (THE       (key     DOOR + |
|     |        his school bag             |             RETREAT)   bowl)    HIS    |
|     |                                   |                        the trip NOTICE |
|     |                                   |                        countdown  |    |
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
(once unlocked). The front door of the living room is the only way out of the house,
and it leads to Act Four. The Retreat has its own music (one slow tune in D major, from
the sound machine) until its batteries are taken: after that the house's tune is heard
up there too.

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
*Plants:* "Daddy's EARLY" (pays off at the end of Act Four). That Dad never asks for
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
Wrong tries:  The study door            -> "Locked. Naturally. And he has left us a notice instead of a key."
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
              sister is holding the key. She fetched it, and she shall turn it." Big Sister: "Mom has
              the key. Technically she outranks the Management."
              The key on the Son's door -> "It doesn't have a keyhole! It has a PASSWORD."
              The key on the front door -> "This door wants a car at the other end of it."
Solution:     As whoever holds the key, use the study door (the key in her pockets is enough; using
              the key on the door does the same). Mom: "'Authorized personnel only.' I authorized
              myself on our wedding day." They all go in.
Gives:        The study. From now on its door is the way into `home-study`.
Plants/pays:  Plants handing things over, which #6 and #8 use, and Act Four's coin depends on.
Notes:        The first time in: Mom, "He has not let me dust in here since March."; Big Sister
              points out the computer and the "family vault"; Little Sister: "Something's BLINKING!"
              (the answering machine: #8).
```

```
Puzzle #4: The Retreat Goes Dark        (Home · Lead: Little Sister, then Big Sister · her fort, and the attic)
Needs:        nothing
Setup:        The closet under the stairs is too dark to find a plug in (#5), and Little Sister will not
              go in without her own flashlight. It lives just inside her blanket fort, in her room,
              where nobody but she may go: "NO BIG SISTERS" is her sign, and her rule.
Wrong tries:  Mom or Big Sister at the fort, or at the flashlight -> "One does not enter a lady's fort
                                             uninvited." / "'NO BIG SISTERS.' I respect a posted boundary."
              A dead flashlight at the closet -> "Not with a DEAD flashlight! It's dark in there. It
                                             wants batteries first. THEN I'll go in."
              Big Sister at her sound machine, before there is a dead flashlight in the house -> "It
                                             stays on. Tonight of all nights. It is the only one of us
                                             that is calm."
              Mom at the sound machine     -> "The batteries are in there, and they are not mine to take.
                                             Not from a daughter. Your sister must do this herself."
              Little Sister at the sound machine -> "The batteries are IN there! But I can't touch it.
                                             Rule AND treaty. She has to. It's HER music box."
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
              ("You will, darling. Often. And each time I shall say thank you, and mean it.")
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
                                             my flashlight. MINE. The pink one. It lives in my fort."
                                             She will not go in again without it.
              Little Sister, when one of the others is holding it -> "I need my flashlight BACK.
                                             Somebody's got it who isn't me."
              The computer upstairs, before this is done -> "No internet."
Solution:     With her flashlight working (#4), Little Sister goes into the closet. "Flashlight ON.
              There's the vacuum. And Daddy's golf sticks. And a plug that isn't plugged into
              anything!" Mom talks her through the socket. The little light goes from red to green.
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
                                              "There is exactly one pencil in this house that can ever
                                              be found. It is on your father's crossword."
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
              Mom: "Seventeen seventy-six." -> "No. A matter of record: 1776 is the Declaration, the
                                               Fourth of July. 'We the People' came later."
              Mom: "Seventeen eighty-nine." -> "No. In 1789 the new government began, and General
                                               Washington took the oath. It was written by then."
              Mom: "Let me think about it." -> she leaves the dial alone.
              The study key on the vault  -> "The vault has a dial, darling, not a keyhole."
Solution:     Mom: "Seventeen eighty-seven." "Signed in Philadelphia on the seventeenth of September.
              He does listen. Just not at the time." Inside: her spare car key, two ketchup packets,
              and a card: "KNEW YOU'D KNOW. - THE MANAGEMENT."
Gives:        The spare car key (`home.hasCarKey`).
Plants/pays:  The clue is in the house for a player who does not know: the framed Preamble in the
              living room. Mom, looking at it: "'We the People.' A matter of record: signed in
              Philadelphia, the seventeenth of September, 1787." Pays off "THE MANAGEMENT". The ketchup
              is Dad's running gag (he is saving it; nobody has asked for what).
Notes:        The wrong years cost a line each, and each line is true. "He keeps ketchup in a vault."
```

```
Puzzle #11: Leave For Nevada        (Home · Lead: any of them · the front door)       THE GATE
Needs:        #7, #9 and #10
Setup:        Nothing stops them now.
Wrong tries:  The door, with no dot on the map: Mom -> "Not until we know where we are going. One of us
              in this family must." Big Sister -> "A journey without a destination is just Dad."
              Little Sister -> "Is it a 'mergency?" (The first time, Mom adds why they will want a
              key: "And there is the matter of my car. Your father moved it this morning. My keys left
              in his pocket." Big Sister:
              the spare is in the family vault. Little Sister: "It's a box with a clicky wheel!")
              The door, with the dot and no message: Mom -> "There is a message on your father's
              machine upstairs, and I would like to hear it first."
              The door, with both and no key: Big Sister -> "Destination: yes. Message: yes. Car key:
              no. Two out of three does not start an engine."
Solution:     Open the door. Mom: "One moment. In this family nobody starts a journey without the
              psalm." Big Sister: "Psalm 121. Verse 8." Little Sister, by heart: "The LORD shall
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

- **The Son's door** (the landing). His toy alarm asks for the password, in his own
  recorded voice. Little Sister knows it, because she has watched him, and does the
  voice: "The password is: I still want a dog." It lets her in. Mom, quietly: "Not
  tonight, sweetheart. I am not ready to look at that room with nobody in it." The door
  stays shut all act. It is the one place the act is allowed to be sad.
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
  the truest thing in the room, once: "The Lord's own picture of Himself: 'even as a
  hen gathereth her chickens under her wings'. Matthew 23:37." "Tonight I know just how
  the hen feels."
- **The Retreat.** Little Sister takes her boots off with great ceremony and whispers
  at full volume ("THIS IS MY WHISPER."). Mom: "Soft light, one sound, nothing out of
  place. Darling, it is a set. It is a very good set." She can name the key the music
  is in (D major). The rules, close up: THE RETREAT. 1. SHOES OFF. 2. VOICES DOWN. 3. NO
  CHICKENS; and under the third, in crayon, AN APPEAL HAS BEEN LODGED. ("You have not
  made a room. You have founded a republic.") The room is perfectly calm and Big Sister
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

The middle of Nevada, the next morning.

## Characters

- THE OLD-TIMER: sells rocks and lemonade at the last stop before nothing; saw the low sun flash off the wagon and the sky open where the flash fell, and has told everyone he saw nothing; wants to be asked nicely.
- THE MAN IN GRAY: stands in front of a government notice; can neither confirm nor deny the fence; wants nobody to read what is behind him, and is no match for a seven-year-old.
- MOM, BIG SISTER, LITTLE SISTER: as before, with lemonade.

## Puzzle structure

```
              Cut-scene: Where the map stops
                            |
            +---------------+----------------+
            |                                |
   #5 Ask Nicely                  #7 Ask Two Hundred Questions
       (Mom)                           (Little Sister)
            |                                |
   #6 Hand Over The Coin          #8 Read The Notice
   (Mom gives it, Big Sister            (Big Sister)
    knows what it is)                        |
            |                                |
            +---------------+----------------+
                            |
            #9 Flash The Coin Where The Tracks Stop      the gate
               (whichever of them holds the coin)
                            |
                  Cut-scene: Some when
```

Goal of the act: **find out what happened to them.** Chain A is the witness and what he
gives them. Chain B is the closed area and what the notice says. Each chain ends with
Big Sister holding half of the answer. The gate is where the halves are put to use: the
witness's story says what opens the door, and the coin is the thing to do it with.
A little harder than Act Three: each chain takes two of the three.

**The rule of the doors**, the same in every era (it is Act One's and Act Two's, and is
written out in [PUZZLES-rome.md](PUZZLES-rome.md)): a door in time stays where it once
opened, shut and invisible, and it hums. Light thrown on the place opens it, and the
more light, the bigger the door. Dad learns it in the pyramid with a flashlight and a
sunbeam. The Son learns half of it in Rome with a coin. Mom and the girls are never
told it. They have an old man who saw the low sun flash off the wagon and the sky open
where the flash fell, and does not know which part of his story matters; a hum, where
there is nothing to hum; a low morning sun; and a coin so new it shines.

## Location layout

```
+--------------------------------------------------------------------------+
| THE LAST STOP BEFORE NOTHING            mesas, far off                   |
|                                                                          |
| the road      LAST STOP                          the FENCE ............. |
| GAS (crossed  shack       gas    LEMONADE        its corner   the NOTICE |
| out), ROCKS,              pump   STAND, under    a traffic    on it:     |
| LEMONADE                         an umbrella     cone         AREA CLOSED|
|                           THE OLD-TIMER                 THE MAN IN GRAY  |
|                           (in a lawn chair)             - in front of    |
|                                                           the notice, or |
| Mom's car                                               - backed off     |
| (its tail off                                             along the fence|
|  the picture)                          the tire tracks run out from      |
|                                        under the fence, and stop at      |
|  Here: Mom, Big Sister,                A PATCH OF GLASS. Nothing to see  |
|  Little Sister                         over it. It hums.      rusty drum,|
|                                                               sagebrush  |
+--------------------------------------------------------------------------+
```

One location, one painting (`art/scenes/nevada-roadside/`). Behind the fence, out of
reach: the closed area, and the rest of the tire tracks. The low morning sun is to the
right and a little behind us, so shadows fall to the left, and the glass lies in it.
Nobody can walk onto the glass: Mom has said so, and routes go round it.

## Cut-scenes and puzzles

```
Cut-Scene: Where the map stops        (opens the act)
```
A dirt lot. Mom: "Thirty-seven miles past Last Gas. This is where the map stops." Big
Sister has a fact about Nevada. Little Sister: "It's all DIRT. Who ordered this much
dirt?" Mom: "Somebody here saw something. We will ask nicely."

```
Puzzle #5: Ask Nicely        (Nevada · Lead: Mom · the lemonade stand)
Needs:        nothing
Setup:        One witness: an old man who has watched this road for forty years and tells everybody he
              did not see nothing. Men in gray suits have already been asking.
Wrong tries:  Little Sister asks          -> "Lemonade's a dollar, little miss. Stories are extra."
                                             "I don't HAVE a dollar. I have a tooth."
              Big Sister asks             -> she cross-examines him. "That is a double negative. Technically,
                                             you saw something." "Technically, I'm closed."
              Mom: "A sensible silver sedan."         -> "Nothing sensible came down this road yesterday."
              Mom: "A black car with dark windows."   -> "That's what the gray suits drive. Try again."
Solution:     Mom says good morning, and asks to buy three lemonades and a few minutes of his time. Nobody
              has said good morning to him in forty years. He will talk to family, so he tests her: what
              were they driving? "A red station wagon with wood on the sides and far too much luggage on
              the roof." He tells her: the driver waved. "Sun was low. Hit the chrome on that wagon and
              threw a flash up ahead, like a signal mirror. Right where it landed, the sky opened up like
              a tin can. The road sign changed its mind. And that wagon drove straight in." An hour later
              the gray suits put up a fence. "Radiation," they say. It is the third piece of desert they
              have shut this year.
Gives:        The witness's account. A silver coin that fell out of the sky this morning and hit his hat.
Plants/pays:  Pays off the intro (the sign that changed its mind) and the look of the wagon. The coin is
              the one the Son tossed through the coin-sized door in Rome: the other side of that door is
              high over this desert ("Why is the sky DOWN?"). Plants the flash of low sun, which he tells
              without knowing it is the part that matters: it pays off in #9. (Ask him again, as Mom:
              "Low sun on bright chrome, ma'am. One flash, up ahead. And where it fell, the sky came
              open. Never seen the like.") Plants the Geiger counter that never clicks (ask him again,
              as Mom or as Big Sister): the radiation is an excuse.
Notes:        This is the author's "finding witness and finding out there have been government areas that
              have been shut down in the desert due to elevated radiation levels". Courtesy is the key,
              and knowing her husband's car is the lock.
```

```
Puzzle #6: Hand Over The Coin        (Nevada · Lead: Mom, then Big Sister)
Needs:        #5
Setup:        Mom has a coin she cannot read: "It looks old and it looks new. Your sister will know which."
Wrong tries:  Give it to Little Sister    -> "A money! With a grumpy man on it. Can I buy a lemonade with it?"
                                             (She can pass it on.)
              Offer it back to the old-timer -> "He gave it to us, darling. It would be rude to give it back."
              Talk to Big Sister with the coin -> "Then hand it over, Mother. I can't footnote what I can't hold."
              Show it to the man in gray  -> "I can neither confirm nor deny that that is a coin."
                                             "If it were a coin, I would have to file a report. So it is not a coin."
Solution:     Hold the coin and click Big Sister (or her portrait). "Mother. This is a Roman denarius. And that is Julius
              Caesar. Fun fact: in 44 B.C., coins were struck in Rome with Caesar's own portrait. While
              he was alive. And it isn't two thousand years old. Look at the edges. It is NEW. It has
              hardly been in a pocket."
Gives:        Half the answer: a new coin from 44 B.C.
Plants/pays:  Pays off #2 (handing things over) and the Son's coin toss in Act Two. Plants that the coin
              is new, which is to say that it shines: #9.
Notes:        A thing sent through a hole in one year comes out of a hole in another. This is the first
              time one half of the family helps the other without knowing it.
```

```
Puzzle #7: Ask Two Hundred Questions        (Nevada · Lead: Little Sister · the fence)
Needs:        nothing
Setup:        There is a notice on the fence. A man in a gray suit is standing exactly in front of it.
Wrong tries:  Read the notice             -> each of them can see AREA CLOSED above his shoulders and none
                                             of the small print, and says so. Big Sister: "I can read
                                             'AREA CLOSED'. The small print is behind his jacket."
              Mom asks him to move        -> "There is no notice, ma'am." "I can see all four corners of it."
                                             "I can neither confirm nor deny a corner."
              Big Sister asks on what authority -> "I can neither confirm nor deny that it is an area."
                                             "It has a fence." "I can neither confirm nor deny the fence."
Solution:     Play as Little Sister and talk to him. "Why is your tie gray? Is your car gray? Is your DOG
              gray? Do you have a dog? What's his NAME? Why are you standing there? Is it your turn?"
              He retreats along the fence with a hand to his ear ("Sir? I have a situation. She is about
              seven.") and she goes with him.
Gives:        A clear view of the notice. He stays busy for the rest of the act.
Plants/pays:  Pays off "ask a LOT of times". Looking at the fence, she says: "I could fit under that.
              ...I'm just SAYING." That is for the next act.
Notes:        Courtesy cannot move him, and neither can logic. The notice itself says "No questions."
```

```
Puzzle #8: Read The Notice        (Nevada · Lead: Big Sister · the fence)
Needs:        #7
Setup:        The notice can be read now: AREA CLOSED. BY ORDER. ELEVATED RADIATION LEVELS.
              SECTORS 44 AND 2560 SEALED UNTIL FURTHER NOTICE.
Wrong tries:  Mom reads it                -> she reads it out. "Sectors. As though the desert had been
                                             numbered. Your sister should see this."
              Little Sister reads it      -> "A, R, E, A. And a yellow spinny flower. 'Radiator levels.'"
Solution:     Big Sister reads it. Radiation is easy to believe in Nevada: atomic bombs were tested here
              from 1951 until 1992. "Which makes it a very good excuse. But look at the sectors. Forty-four.
              Twenty-five sixty. Nobody numbers sectors like that. Those aren't places, Mother. I think
              those are years."
Gives:        The other half of the answer.
Plants/pays:  44 and 2560 are the years the Son and Dad are in. Whoever put up the fence knows that.
Notes:        Whichever of #6 and #8 comes second, she joins them up on the spot: "Sector 44. A new coin
              from 44 B.C. It is the same forty-four. The holes don't go to places. They go to YEARS."
```

```
Puzzle #9: Flash The Coin Where The Tracks Stop        (Nevada · Lead: whoever holds the coin · the patch of glass)       THE GATE
Needs:        #6 and #8
Setup:        Tire tracks run out from under the fence and stop at a patch of sand that has turned to
              glass. There is nothing else to see. Little Sister, looking: "The ground is SHINY. And it
              hums. Like a bee in a jar, but there's no bee. And no jar."
Wrong tries:  Go to the tracks before both halves: Mom -> "I would like to understand it before any of
              us stands on it." Big Sister -> "A theory is not a fact until I can footnote it."
              Little Sister -> "Can I jump on it? ...Mommy's doing the eyebrow."
              The coin at the tracks before both halves -> the same.
              Go to the tracks after both halves, with nothing in hand -> she listens, and remembers
              the old man. Mom: "It hums, darlings. Very quietly, like your father when he is lost and
              will not say so." "The gentleman said a flash of low sun fell just here. I wonder what we
              have that flashes." Big Sister: "A flash of low sun fell here, and the sky opened. That
              is his whole story. So: we need a flash." Little Sister: "The wizard said the car went
              FLASH and the sky went OPEN. I want to do a flash!"
Solution:     Use the coin where the tracks stop, as whichever of them is holding it. She goes to the
              corner of the glass, the other two stand back, and she holds the coin up to the low sun.
              Mom: "Stand back a little, darlings. I am about to do something your father would think
              of." Big Sister: "A low sun. A new coin. And an old man's story. This is called an
              experiment." Little Sister: "I'm gonna do a FLASH! Like the car did! Everybody WATCH!"
              One flash. The light stays where it fell, over the glass, and a door opens there, exactly
              the size of the coin.
Gives:        A door in time the size of a coin, and the closing scene.
Teaches:      Their half of the rule of the doors: light opens them. (A coin's worth of light, a coin's
              worth of door: they have not been told that yet, and Mom's last line knows it anyway.)
Hints:        Mom: "A flash of low sun opened the sky where the tracks stop. We have a low sun, and a
              very new coin." Big Sister: "A flash of sun opened it once. The sun is low again, and the
              coin is new enough to flash. Where the tracks stop." Little Sister: "The shiny money can
              do a FLASH! Like the car did! At the hummy place, where the car tracks stop!"
Plants/pays:  Pays off the old man's flash (#5), the newness of the coin (#6), and the Son's "little
              light, little door" in Rome, which nobody here has heard.
Notes:        Any of the three can do it, and each has her own line: the coin can be handed round
              first. Until this moment there is nothing of the door on the screen. The light is drawn
              live: the flash of the coin (`#spark`), a short beam (`#ray`), the spot where it lands
              (`#glint`), and the game's own wormhole at a radius of 10 on a dark disc (`#hole`, in
              `#door`), all out of sight until the coin goes up.
```

```
Cut-Scene: Some when        (closes the act)
```
Little Sister is at the door before anybody can say no: it is at the height of her eye.
"A HOLE! In the AIR! And it's LITTLE! It's littler than ME!" Big Sister narrates it:
"'The air,' she noted, 'now had a hole in it. A hole exactly the size of the coin.'"
Little Sister, with her eye to it: "It's a DIFFERENT sunny in there! And it smells like
SAUSAGES!" Mom: "Sausages. She is quite right. And bread, and woodsmoke. And I believe I
can hear chickens." Big Sister: "It is morning in there, too. I do not think it is THIS
morning." "Then which morning, darling?" She gives both: "Sector 44: forty-four B.C. The
year Julius Caesar was killed, on the Ides of March." "Sector 2560: twenty-five sixty
B.C. About when the Great Pyramid was finished." "They didn't crash, Mother. They didn't
go anywhere. They went some WHEN." Little Sister, turning round to them: "I TOLD you!
Daddy's not lost! Daddy's EARLY!" Big Sister: "...More than four thousand years early.
She was right. I need to sit down." Mom: "Then we know where they are. And we have a
door. It is only a little small." "Girls. We are going to go and bring them home."

"Daddy's EARLY" is the top of the scene, and is word for word the line the author asked
to keep. Three lines follow it, as before.

*What comes through the door, and why it is so little.* A different sunlight; the smell
of sausage, bread and woodsmoke; chickens. That is a March morning in Rome in 44 B.C. as
Act Two has it (the snack bar's bread and sausage, the soothsayer's sacred chickens on
the temple steps), and it is all they get. They do not see the Son, hear him, or learn
which of the two years is in there: Big Sister names both and chooses neither. The
player, who has been to Rome, knows more than the family does.

*Plants:* the way through is here, it is too small, and somebody official is standing
a few steps from it with his back turned, reporting a seven-year-old to his superiors.

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
| Silver coin | The Son takes it from a fountain in Rome, opens a door the size of it with the morning sun, and tosses it through (Act Two). It hits the old-timer's hat in Nevada. | The Son; then Mom, and whoever she gives it to | Act Four #6: only Big Sister knows what it is. Act Four #9: any of them can flash the sun off it |

The five things from the house that are not used up (the key, the flashlight, the note, the pencil, the car key) are still in their pockets in Nevada. The batteries are in the flashlight.

**Plants and payoffs**

| Planted | Where | Pays off |
| --- | --- | --- |
| "Daddy's not lost. Daddy's EARLY." | Opening of Act Three | The last scene of Act Four |
| Dad never asks for directions | The voicemail; Little Sister's postscript to the prayer ("please make Daddy ask for directions. Just ONE time."); the wedding photograph on the landing | Act Three #7, the wedding question. (Draft: the last thing Dad does in the game is ask for directions. That would also be a seven-year-old's prayer answered.) |
| "THE MANAGEMENT" | Act Three #1, Dad's notice | Act Three #10: the vault's label ("Your mother will know. She brings it up.") and the card inside it ("KNEW YOU'D KNOW.") |
| "I FIT!" | Act Three #2 (under the keyboard) and #5 (the closet) | The fence: "I could fit under that." For the next act. |
| Handing a thing to someone | Act Three #3 (the key), #6 (the note), #8 (the pencil) | Act Four #6 (the coin) |
| The road sign that changed its mind | The intro | Act Three #9: "That sign just changed its--". Then the old-timer's account, Act Four #5 |
| 5:41 on the tape; 5:47 on the map | Act Three #9 and #7 | Whichever comes second: Big Sister counts the six minutes |
| "Thirty-seven miles past Last Gas" | Act Three #7 (the map) and #9 (Dad says it himself) | The first line of Act Four |
| The ketchup packets Dad is saving | Act One (his running gag) | Act Three #10: two of them are in the family vault. Nobody has asked what he is saving them for. |
| "I still want a dog" | Rome, Act Two: "Edge, we get a dog." | Act Three: it is the password on his bedroom door. Not yet answered. |
| Psalm 121:8: "thy going out and thy coming in" | Act Three #11, at the front door. Mom: "Going out, and coming in. All five of us." | Not yet: the coming in. (Mom's "My times are in thy hand", Psalm 31:15, belongs to the end of Act Four.) |
| Little Sister's flashlight | Act Three #4 and #5 | Act Four: light opens doors in this story, and hers is too small to be seen in the morning sun. For later. |
| "Chickens KNOW." | Act Three, Little Sister at her flock | The geese in Egypt, the sacred chickens in Rome, the old-timer's hens in Act Four: in every era the birds face a door in time before any person has noticed it. |
| General Feathers' place on the pillow: RESERVED | Act Three, Little Sister's room | She is in Dad's suitcase in Egypt (Act One), in charge. Not yet: her coming home. |
| 1921 B.C. and 44 B.C. on Big Sister's timeline | Act Three, the Retreat | The two sectors on the notice in Act Four. "Her timeline has that year on it." |
| "The Retreat goes dark so that the internet may live." "I intend to mention this again." | Act Three #4 | Not yet. She will. |
| The appeal lodged against rule three (NO CHICKENS) | Act Three, the rules in the Retreat | Not yet heard. |
| The coin that "didn't come back down" | Rome, Act Two | #5 and #6 |
| "Sun was low. Hit the chrome on that wagon and threw a flash up ahead, like a signal mirror." | #5, the old-timer's account | #9: the coin, held up to the low morning sun |
| "Look at the edges. It is NEW." | #6 | #9: a new coin shines |
| "Why is the sky DOWN?" | Rome, Act Two, looking through the coin-sized door | #5: the coin fell out of the sky and hit his hat |
| A Geiger counter that never clicks | #5, ask again as Mom or as Big Sister | Not yet. The radiation is an excuse: for what? |
| Sectors 44 and 2560 | #8 | Not yet. Who numbered them, and how many more are there? |
| A hum where there is nothing to hum | #9, before the coin goes up | #9. It is the door, shut. |
| A door the size of a coin, with a morning in it | The closing scene | Not yet. It is the way through, and it is too small. More light would be a bigger door: they have not been told. |
| Sausages | The closing scene: the first thing Little Sister notices | Not yet. Her brother is on the other side of a door like this one, and he found Rome's snack bar the same way: "Step one, I can SMELL you." |

(The last nine rows are Act Four's, and their puzzle numbers are that act's own.)

**Facts used.** In Act Three the riddle (#1: a piano's eighty-eight keys), the password
(#6: sliced bread, 1928), the tape (#8: a cassette can be wound with a pencil) and the
vault (#10: the Constitution signed in 1787, the Declaration adopted in 1776, the new
government and Washington's oath in 1789) rest on real history; so do the things Mom
and Big Sister say for the pleasure of it (Luther's hymn, Abigail Adams's letter,
Washington's Rules of Civility, Adams and Jefferson, Bach's "S.D.G.", Cristofori's
piano, what B.C. and A.D. mean, the year Archbishop Ussher's book was published). The
years before Christ on Big Sister's timeline (4004, 2348, 1921, 1491) are the Bible's
count, as Ussher counted it: the author's rule for the whole game. Six verses of
Scripture are quoted, and nine words of a seventh (Matthew 23:37), from the King James
Version, each with its reference. In Act Four the bomb tests (#8), the coin (#6)
and the two years (the closing scene) all rest on real history. The lists, and which
of them have been checked against a source, are at the end of
[CHARACTERS.md](CHARACTERS.md): Big Sister's facts, Mom's facts, and the verses. Two of
Act Four's were reworded on 2026-10-07 to say less and be surer: of the coin, only that
in 44 B.C. coins were struck in Rome with Caesar's own portrait while he was alive (not
that he was the first); of 2560 B.C., only "About when the Great Pyramid was finished."
One of Act Three's was reworded the same day on the fact-checker's finding: a cassette
is wound with "a pencil", and nobody says that the pencil's six sides are why it fits.

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
plays it three ways on a stand-in for the engine. `briefs/out/nevada-play.py` plays it
three ways in the real game by real clicks, with a different one of the three holding
the coin at the end each time, and keeps a picture of every moment worth looking at in
`briefs/out/nevada-shots/`.

## What comes next (not written)

- How Mom and the girls follow. The door is open and the size of a coin. More light is
  a bigger door, and nobody has told them so: the old man's story has it (a whole low
  sun on a whole chrome bumper, and a door a station wagon could drive into), and so
  does Mom's car, which has mirrors.
- The man in gray is a few steps away. What he does when he turns round.
- Whether the door gives onto 44 B.C., onto 2560 B.C., or onto neither. Big Sister has
  named both and chosen neither; the sausages are a clue the player can read and the
  family cannot.
- What the men in gray know, and whether they are after the same thing.
- When the two halves of the family first hear from each other. The coin went one way
  by accident. Something could go the other way on purpose: the Son, in Rome, is
  standing beside a door the size of a coin with nothing left to send through it.
- Little Sister eyed the fence: "I could fit under that." Still for later.
