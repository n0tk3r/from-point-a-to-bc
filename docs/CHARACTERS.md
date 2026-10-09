# From Point A to B.C.: the character bible

Who everybody is, what they want, how they talk, what they do in play and how they
look and move. Anyone writing a line, a puzzle or a picture for the game starts here.

The five members of the family and their traits come from the game's author. The
details hung on those traits (the wants, the fears, the running gags, how each one
changes) are a first draft, marked **draft** where they are invention, to be kept,
changed or thrown out. Every quoted line is in the game now, in
`js/content/lines.en.js`.

Nobody has a name yet. On screen they are Dad, Son, Mom, Big Sister and Little Sister,
and they call each other what families call each other.

## The family at a glance

| | Age | In one line | What they do that nobody else can |
| --- | --- | --- | --- |
| **Dad** | grown-up, allegedly | Took a shortcut. Still thinks it was a good one. | Improvises, and talks his way sideways |
| **Son** | about ten (draft) | Zany and silly. Treats being lost in time as the best field trip ever. | Pokes at everything, fears nothing, makes friends in any century |
| **Mom** | grown-up, actually | Classy, refined and loving, and not leaving without her family. | Adults listen to her. Courtesy opens doors. She knows her husband by heart. |
| **Big Sister** | 13 | Brilliant. Plays the piano, reads and writes books, remembers history. | Knows the fact that cracks the puzzle |
| **Little Sister** | 7 | Small but mighty. Loves chickens above everything. | Fits where nobody else fits, and can distract anybody. Knows chickens, and is always right about them |

Two stories run side by side. **Dad and the Son** are lost in the past, apart from
each other, and their puzzles reach across time. **Mom and the girls** are in the
present, together, working out what happened. Their puzzles are detective work, and
each one needs the right person: find the fact, get the grown-up to talk, get into the
small place.

## Rules for every line

- **A line belongs to one person.** If it could be said by anybody, rewrite it until
  only one of them could have said it.
- **Funny comes from character.** Dad puns, the Son swerves, Mom understates, Big
  Sister footnotes, Little Sister declares.
- **Nobody is mean.** They tease, they bicker, they are never cruel, and none of them
  is ever the butt of the game's own joke.
- **Every fact Big Sister states is true.** Check it before it goes in. Real history
  is the game's rule book. The list is [at the end of this document](#big-sisters-facts).
- **Short.** One thought to a line, two lines at most before someone else speaks.
- **The family is American.** Gray, tire, sedan, mailbox, Mom.
- **All of it is original.** No lines, names or jokes from any other game, book, film
  or show.

## The family's faith, and how it is written

They are a Reformed Christian family who love Jesus. It is simply part of how this
household lives, the way music is: grace is said, Sunday is church, the children know
their verses, the Bible by Dad's plate is read after supper, and when Dad does not come
home the first thing Mom does is pray. Write it the way such a family would recognise
themselves: warm, natural and unselfconscious.

- **Never a sermon, and never a joke at its expense.** Nobody preaches to anybody, on
  screen or at the player. The comedy stays where it always was, in character: Little
  Sister adds her own postscript to a prayer; Big Sister knows the chapter and verse.
- **Scripture is quoted from the King James Version only: exactly, briefly (a phrase or
  one verse), with its reference said or shown.** LORD is in capitals where the King
  James text prints it so. Scripture is never a pun, a password, a combination or a
  riddle. It is said because it is true. The verses the game quotes are listed
  [at the end of this document](#scripture-quoted-in-the-game).
- **Hymns and songs are named, never quoted.** No line of any hymn, song, poem or play
  appears in the game. If someone sings words, they are words written for the game.
  (Mom plays "A Mighty Fortress Is Our God", and names it. The few notes the game plays
  are its own tune, written for it.)
- **Prayer is short, sincere and in their own words.** They bow their heads and fold
  their hands (the pose `actor.pray` in a script).
- No catechism lines yet: the author will say which one his family uses.
- God's care over time is the family's quiet answer to the whole story: "My times are
  in thy hand" (Psalm 31:15). That line belongs to Mom at the end of Act Four
  (`nevada.gate.5b`). At home, the psalm for a journey is Psalm 121.
- The Bible's history is history, on the same timeline the family is scattered along.
  Big Sister's wall timeline (in her attic, the Retreat) is where the game says how it
  counts the years, and what B.C. and A.D. mean: see the next section.
- The one place in the house that is allowed to be sad is the Son's door.

> "Father, You know where they are tonight, and I do not. Keep them."
> "And please make Daddy ask for directions. Just ONE time. Amen."
> "'The LORD is my shepherd; I shall not want.' Psalm 23. I know ALL of it. ...I do want Daddy, though."
> "You may say it whenever you like, my love. It is not the clock He is listening for."
> "The Lord's own picture of Himself: 'even as a hen gathereth her chickens under her wings'. Matthew 23:37." "Tonight I know just how the hen feels."
> "And thank You for the lemonade. And tell Daddy we're COMING, so he doesn't have to be brave by himself. Amen."

---

## How the game counts the years

The author's rule, in his words (7 October): "always use bible geneology dating and
biblical dating." So **every date before Christ in this game is counted from the Bible's
own genealogies, as Archbishop James Ussher counted them** (his Annals, 1650). The family
holds this simply, as a family that reads its Bible does. It is never argued about on
screen, nobody in the game mentions textbooks, and nobody sneers at anybody. It is just
how the years are counted.

The years (these, and no others, for anything before Christ):

| Year | What |
| --- | --- |
| 4004 B.C. | Creation |
| 2348 B.C. | The Flood |
| after that | Babel, and the scattering of the nations. Egypt is settled by Mizraim, Noah's grandson (Genesis 10:6): "about 2188 B.C." |
| 1921 B.C. | Abram leaves Haran; that same year a famine sends him down into Egypt (Genesis 12:10) |
| 1706 B.C. | Jacob and his family come down to Joseph in Egypt |
| 1571 B.C. | Moses is born |
| 1491 B.C. | The Exodus |
| 1012 B.C. | Solomon begins the Temple |
| 44 B.C. | The Ides of March (Rome's own date: the same in every count) |

- **Where the Egypt date comes from.** The Egypt act is set "about 1920 B.C.", and the
  number on the notice in Nevada is 1921. The Bible gives no date for the pyramids and
  never mentions them, and nobody in the game says it does. The game places the building
  of the Great Pyramid beside Abraham on the reckoning of Answers in Genesis (The New
  Answers Book 2, chapter 24: its table sets Khufu and the fourth dynasty beside
  Abraham) and of Creation Ministries International (the great pyramids "probably fit
  in a small window around Abraham's lifetime"). So when Dad stands at the foot of the
  pyramid, Abram and Sarai are in Egypt (Genesis 12:10-20).
- Textbook dates for early Egypt are different (they put the Great Pyramid at about
  2560 B.C.), and the game does not use them.
- From the present day (A.D. 2026) back to 1921 B.C. is 3,946 years: "nearly four
  thousand years". From 1921 B.C. to 44 B.C. is 1,877 years: "nearly nineteen hundred
  years". Nobody says "about 2560", "four and a half thousand years", or anything about
  millions of years.
- **The doors in time open on years that matter.** 44 B.C. is the Ides of March. 1921
  B.C. is Abram in Egypt. Big Sister notices it once, at the end of Act Four ("The Ides
  of March. Abram in Egypt. The holes open on years that MATTER. ...I don't know why.",
  `nevada.gate.2f`). Nobody explains it yet.
- **Where the game says it.** Big Sister made her timeline with Ussher's dates, and says
  so once: "I used Archbishop Ussher's dates. He counted the years from the Bible's own
  genealogies." (`home.timeline.1`). The first time any of the three looks along it they
  read it between them (`home.timeline.1` to `.6`, then the red mark and what B.C. and
  A.D. mean): 4004, 2348, 1921, 1491 and 44 B.C. are named there, and no others. Mom's
  "A matter of record" is that the Archbishop's book was published in 1650. Little
  Sister notices how little paper there is before Abram, and her sister answers: "It
  is as long as it was." That is all the comment the dates get, anywhere. In Act Four Big
  Sister names 1921 B.C. again, from her timeline, and says how far back it is ("Nearly
  four thousand years early"): dates stated as plain fact, not comment.
- Any of the family may state a date from the table as plain fact. Each such line is in
  the facts tables at the end of this document with its source given as "The Bible's
  count (Ussher)".

---

## Dad

**Who he is.** The driver of the shortcut. Cheerful, stubborn, and certain about
everything, including the things he is wrong about. He leads in the past.

**Wants.** His son back, everyone home, and for it never to come up that he was lost.

**Fears.** That this is his fault. (It is.) Asking for directions.

**Gets wrong.** He treats 1920 B.C. like a rest stop with poor signage.

**How he talks.**
- Dad jokes, delivered straight. The turn comes in the last three words.
- Understatement. A hole in time is "weather, probably".
- He talks to objects, and calls the car "she".
- Short sentences. He never explains a joke and never laughs at one.
- He is kind to everyone he meets, in every century, as if they were neighbors.

**Running gags.** Shortcuts. "Making good time." Manuals read halfway. The ketchup
packets he is saving. Everything he cannot explain is the wind. He has never asked for
directions: he promised.

**In play.** He makes tools out of what is in the car and talks his way round people.

**How he looks and moves.** Yellow flowered vacation shirt worn loose over a stomach,
olive shorts, striped socks, sandals. Brown hair slicked back and to the side, green
eyes, stubble and a short beard along the jaw and chin (no moustache). He walks like a
man who knows where he is going. When he talks he nods, makes a point, shrugs, or puts a
hand on his hip.

**How he changes (draft).** The last thing he does in the game is ask for directions.

> "Maps don't know about shortcuts."
> "Either that's the Nile or a very committed car wash."
> "It shrinks every time I get close. I have the same effect on waiters."
> "'You've reached Dad. I can't pick up right now. I'm either driving or lost.'"
> "'And I am never lost. So: driving. Leave a message.'"

---

## Son

**Who he is.** Zany and silly. He lands in other centuries on his own and is thrilled
about it. Under the noise he misses his dad.

**Wants.** To find Dad, and to see absolutely everything on the way. A dog.

**Fears.** Being bored. Being alone, which he covers by being loud.

**Gets wrong.** Plans: he starts the second one before the first has finished.

**How he talks.**
- **Every line swerves.** It starts somewhere sensible and ends somewhere else.
- Sound effects, made-up words, and a name for everything he meets.
- He scores things out of ten, and calls his plans "Operation" something.
- Kid logic that turns out, annoyingly, to be right.
- Capitals for one word at a time, not whole sentences.
- Never sarcastic. He is delighted, not cool.

**Running gags.** Snacks. Scores out of ten. "Operation." His list of Things Dad Says
Are The Wind. "Are we when yet?" The dog he is hoping for (it is also the password on
his bedroom door at home, which says NO GIRLS ALLOWED and is booby-trapped: a toy alarm,
"Operation No Girls", and a toy blaster in the slot over the door).

**In play.** He pokes, climbs, trades and befriends. He fits where Dad does not.

**How he looks and moves.** Blonde hair under a red cap, blue eyes, blue hoodie, purple
backpack, navy shorts, sneakers. He walks with a bounce, fists pumping and head going
from side to side. When he talks he points, throws both arms up, waves both hands, or
shrugs.

**How he changes (draft).** He learns to finish one plan before starting the next.

> "Everyone here is wearing a bedsheet. Ten out of ten. Biggest sleepover in history."
> "Operation Borrow-A-Wish is GO. Splish."
> "It hums. Dad says it's the wind. Dad says EVERYTHING is the wind. I have a list."
> "Heads, I find Dad. Tails, Dad finds me. Edge, we get a dog."

---

## Mom

**Who she is.** Classy, refined and loving. She keeps her voice down and her
standards up, and she is the calm at the middle of the family. She leads the ones who
stayed behind. She is as clever as her elder daughter, and it is the daughter who takes
after her: Mom's territory is music, the stage, her books, and the founding of the
United States.

**Wants.** All five of them at one table. Everything else is arrangements.

**Fears.** The phone that rings and rings. Not being there when one of them needs her.

**Gets wrong (draft).** She looks for the sensible explanation a little longer than
the facts allow, and she is too polite to interrupt nonsense the first time.

**What she knows and loves.**
- **Music.** The piano is hers. She taught Big Sister, who now plays better. She sings:
  hymns on Sunday and about the house, and anything else when she thinks nobody is
  listening. She hears pitch: the doorbell is a quarter-tone flat, and so is her husband.
- **The stage.** She did theatre all through school, and still does when a church or a
  town will have her. She thinks like a stage manager, and it comes out when things go
  wrong. She can do voices, and can project to the back row without raising her voice.
- **Books.** Lives of the Founders, read the way other people read thrillers. Plays. Poetry.
- **The Founders and the United States.** She loves her country knowledgeably: the
  Declaration, the Constitution ("We the People" is framed in the living room, and she
  can recite it), the letters of John and Abigail Adams, General Washington's rules of
  civility. She corrects the popular version of a story, kindly, when it is wrong.
- **Her faith.** She prays before she does anything else, and without fuss. She knows a
  great deal of Scripture by heart, and quotes it exactly and sparingly, when it is the
  truest thing to say. (See [the family's faith](#the-familys-faith-and-how-it-is-written).)

**How she talks.**
- Whole sentences, well made, and she does not shorten her words: "May I", "I would like", "Let us".
- Endearments: darling, sweetheart, my love. She uses them most when she is worried.
- She understates. Where another person would shout, she gets quieter and more exact.
- She counts her worries precisely: the ninth voicemail, the twelfth look out of the window.
- Courtesy with steel inside it: perfectly polite and impossible to get rid of.
- She knows her husband by heart, and speaks of him ("your father") with fond exasperation.
- She never mocks the girls, and she always answers Little Sister's questions.
- **"A matter of record:"** and then something true, where Big Sister says "Fun fact:".
  They enjoy each other's facts, and are a little competitive about them.
- A stage manager's words under pressure: "Places, girls." "That is your cue." "We do
  not stop the show for a missing cast member."
- One touch of what she knows to a line, never three. She is not a lecturer: most of
  her lines stay short and dry.

**Running gags (draft).** Her handbag holds everything that matters. Lists. Addressing
a difficult man as "the gentleman" until he behaves like one. Being the first person
in forty years to say good morning. "A matter of record." Things that are flat (the
doorbell, the clock's tick, her husband, and the hum of a door in time: "Very quietly,
and a little flat."). Her husband signs himself "The Management"; she is what the
Management answers to.

**In play.** Grown-ups listen to her, so she is the one who gets people talking, and
she is the one who knows the answers about her husband and about her country: what he
promised on their wedding day, and the year "We the People" got it in writing. She has
the knack of things from before her daughters were born: she can wind a cassette with
a pencil. She drives. She does not crawl, climb or shout: she has daughters for that.

**How she looks and moves.** An emerald dress with a belt, pearls, long dark brown curly
hair worn down and flowing past her shoulders, brown eyes, low heels, a handbag on her
arm. She stands with her hands lightly clasped and walks without hurry, in short steps,
her arms hardly moving. When she talks she nods, puts a hand to her heart, or holds out
an open hand.

**How she changes (draft).** She learns that there are days when the correct thing to
do is to make a scene.

> "Voicemail. That is the ninth time. I had decided to stop worrying at eight."
> "First things first, girls."
> "He has hidden a key in MY piano."
> "And I cannot reach it. My arms are a civilized length."
> "A lady does not squeeze into closets, darling. A lady has a seven-year-old."
> "He promised me he would never ask for directions. It is the one promise he has always kept."
> "I do not need to hear it twice. He sounded happy."
> "We are going to be perfectly polite, and completely impossible to get rid of."
> "Reformation Day, darling. A matter of record: Martin Luther's ninety-five theses, 1517."
> "Then you have not read one of them. Good morning."
> "Genesis 12. I have known that chapter all my life, darling. I had never once thought of it as a morning."
> "'My times are in thy hand': Psalm 31, verse 15. Every one of the times, darlings. Even that one."

---

## Big Sister

**Who she is.** Thirteen, highly intelligent and talented. She plays the piano
wonderfully, reads everything, is writing a novel, and remembers historical facts the
way other people remember song words. Her mother leans on what she knows.

**Wants.** To be taken seriously. To be the one who works it out.

**Fears (draft).** Being wrong out loud. That being the clever one will not be enough
to bring them home.

**Gets wrong.** People. She can read anything in the world except a room. She
over-explains, and she corrects grown-ups.

**How she talks.**
- Exact, and well read. Dates, places, "technically", "for the record".
- "Fun fact." Then a true one.
- Words a size too big for her, used correctly.
- Dry, not sour. The eye-roll is in the sentence.
- When she is thinking she narrates, like the novelist she is: *"The table," she
  observed, "was set for five. The house was not."*
- "Mom" most of the time. "Mother" when it is serious.
- She is protective of Little Sister and would deny it.

**Running gags (draft).** "Fun fact." Narrating herself. The chapter titles of her
novel change with events. She counts in fours when she is nervous. She packs a second
book in case the first one ends, and then opens neither, because what is happening is
better. Things are not facts until she can footnote them.

**Her room: the Retreat.** For her thirteenth birthday she asked for the attic, and she
has made it, by herself and on pocket money, into a spa retreat: soft light from many
small lamps, one slow tune in D major (from a sound machine that runs on batteries), a
little fountain, plants, rolled towels, an exercise mat, her books arranged by color, her
novel planned on cards over the desk, and her timeline along the wall. It is reached by
the attic ladder, and a notice stands by the hatch: THE RETREAT. 1. SHOES OFF. 2.
VOICES DOWN. 3. NO CHICKENS. (Under the third, in crayon: AN APPEAL HAS BEEN LODGED.) It
is the one calm place in a loud house. Tonight the room is perfectly calm and she is not,
and it annoys her: the fountain sounds like a clock, and she has counted the little
lights in fours. Her mother admires it exactly and briefly, as one performer admires
another's stage: "Darling, it is a set. It is a very good set." Her little sister has
visiting hours, takes her boots off with great ceremony, and whispers at full volume.

**In play.** She supplies the fact: the year behind a password, what a coin is, what a
pair of numbers means. She plays any piano she meets. She notices. At home she gives up
the batteries out of her sound machine for her sister's flashlight, as a sacrifice she
intends to mention again: "The Retreat goes dark so that the internet may live."

**How she looks and moves.** Indigo cardigan with a white collar and cuffs, gray pleated
skirt, white knee socks, long flowing brown hair down her back, parted in the middle
under a headband, with no bangs. No glasses, and nothing in her hands: the reading shows
in how she talks, not in what she carries. She stands holding one elbow, thinking, and
walks with a small, even swing of both arms. When she talks she nods, raises a finger,
puts a hand to her chin, or points.

**How she changes (draft).** She learns to say "I don't know", and that it is where
finding out begins. The first step is at the end of Act Four ("...I don't know why.").

> "Fun fact: sliced bread was first sold on the seventh of July, 1928, in Chillicothe, Missouri."
> "We don't have a destination. A journey without a destination is just Dad."
> "Nobody numbers sectors like that. Those aren't places, Mother. I think those are years."
> "Sector 44. Sector 1921. Years. I am almost certain. 'Almost' is the part I don't like."
> "It is as long as it was."
> "No. ...A little. Do not tell the room."
> "The Ides of March. Abram in Egypt. The holes open on years that MATTER. ...I don't know why."
> "I don't want to go in there. The rug is probably booby-trapped."

---

## Little Sister

**Who she is.** Seven. Small but mighty, and she will tell you so. She has no fear
that she will admit to, no patience at all, and complete loyalty.

**Chickens.** She loves chickens above everything, and after chickens, stuffed animals.
She is the family's authority on chickens, and she is always right about them. Her room
(the one she shared with her sister until the attic was done) is a kingdom of them: the
flock heaped on a beanbag, a tea party round a spotted teapot, a nest in a cardboard
box, a hen house that used to be a dollhouse, a rooster lamp, a chart headed MY
CHICKENS, a fort with a sign that says NO BIG SISTERS, and a door that says BEWARE OF
CHICKENS. Every stuffed chicken has a name and a rank or a job (Admiral Doodle, who is
in charge of mornings; Corporal Speckle; Private Peep; Mrs. Biscuit, who pours the tea;
Henrietta, who sits on the eggs), and a rank goes up each time its holder goes through
the wash. Big Sister has catalogued them all, against her will.

**General Feathers** is her favorite: a white hen, well worn, with a red felt comb, one
button eye sewn back on in the wrong color (blue), and a paper medal on a ribbon "for
bravery". She is a General because she has been through the wash five times. Little
Sister sent her on the road trip in Dad's suitcase, "to keep an eye on Daddy", with a
note in crayon: `DADDY. GENERAL FEATHERS IS IN CHARGE. DO WHAT SHE SAYS.` (Mom found the
first draft.) So at home there is a place kept on a pillow, with a sign: RESERVED. She is
not worried about the General. She is a little worried about Daddy without proper
supervision, which is why she sent her.

**"Chickens KNOW."** Hers, and she says it as a plain fact. In this story a chicken
notices a door in time before any person does: the birds go quiet, will not eat, will
not lay, and all stand facing it. Nobody explains this. She says it first at home, of
her own flock, and it pays off in every other act: the geese in Egypt, the sacred
chickens in Rome, the old-timer's hens in Nevada (`nevada.old.saw.3b`, `.3c`). Keep it
light: a thread, not a lecture.

**Wants.** To help, right now. To be big. A snack. The front seat.

**Fears (draft).** Being left out for being little.

**Gets wrong.** Long words. Distances ("Is Nevada past the mailbox?"). Plans: she has
started before you have finished explaining.

**How she talks.**
- Short, loud and certain. She declares things, and she is often right.
- "I FIT!" "I'm small but I'm MIGHTY." "I'm not scared. I'm BRAVE-scared."
- Spunky. Brave declarations and little challenges ("We'll SEE about that."); orders, to
  the flock, to her sister, to the General in her absence ("Keep an eye on Daddy,
  General!") and to her mother when she can get away with it ("Mommy, sit down. You've
  been standing up since dinner. I'll do the worrying for a while."); she will not be
  left out ("Come ON, everybody. I know the way!"); and she is ready before anyone has
  finished explaining ("I'm ALREADY going.").
- A seven-year-old's logic, stated as law: "NO GIRLS ALLOWED? I'm not a girl. I'm a
  SISTER. That's a whole different thing." She says hi to things and names them (the
  vacuum, the spiders, the dot on the map), counts on her fingers ("THREE fingers past my
  bedtime"), and has one word in a room that comes out nearly right, never more.
- Questions in chains: why, and why, and why.
- She takes everything literally.
- She says the true thing the grown-ups are stepping round.
- "Mommy" and "Daddy".
- Never babyish, never annoying, never the butt of the joke.

**Running gags (draft).** "I FIT!" Her loose tooth, which she will show to anyone, and
which is not allowed out till Daddy is home to see it. The questions. Long words coming
out nearly right, one to a room at most: "radiator levels", "a ENGINEER", "the answer
machine", "I lodged a appeal". "Daddy's not lost. Daddy's EARLY", which turns out to
be exactly true. "Chickens KNOW." The General, who outranks everybody. Her flashlight,
which is pink, lives in her fort, and is dead when it is wanted, because she read to the
flock under the blanket until the batteries ran out.

**In play.** She goes where nobody else fits: behind, under and through. She distracts
people by asking them things until they give up, so that her mother and sister can do
what needs doing.

**In Act Four (round three).** She names everything: the old-timer is the Rock Wizard
("I just decided"), the man in gray is Mister Gray, the place where the tracks stop is the
Hummy Place, the notice's radiation sign is a yellow spinny flower. She counts the man in
gray's questions on her fingers as she asks them ("That's EIGHT fingers. I have TOES
too."), gives him orders ("You stay RIGHT there. Next question."), and will not be left
out ("I get to HOLD it? Finally!"). She is ready before anyone has finished explaining
("So we need a flash. I'm READY."). Her loose tooth is not for sale: it is waiting for
Daddy. And she is right: about the chickens, about the hiding ("Nobody EVER finds me";
her sister: "That is, regrettably, true."), and about Daddy being EARLY.

**How she looks and moves.** Pink overalls with a star on the bib, yellow rain boots,
pigtails with yellow ties, soft blue eyes and a few freckles. She stands with her fists
on her hips and stomps when she walks, arms straight, like a small soldier. When she
talks she throws both arms up, shows her muscles, or points.

**How she changes (draft).** She learns that sometimes the brave thing is to wait.

> "I FIT!"
> "The red light went GREEN! I fixed the internet! I'm a ENGINEER!"
> "That's not an ANSWER. Number two: is your car gray? Three: is your DOG gray? Four: do you HAVE a dog?"
> "I don't HAVE a dollar. I have a loose tooth. But it's not for sale. It's waiting for Daddy."
> "They know something's up. They knew before I did. Chickens KNOW."
> "I'm not worried about the General. I'm a LITTLE worried about Daddy. That's why I SENT her. He needs supervising."
> "THIS IS MY WHISPER."
> "SHH! Everybody SHH! ...CHICKENS. Three! No, FOUR! I can hear CHICKENS in there!"
> "Mommy, I miss General Feathers. But Daddy needs her MORE. She's keeping an eye on him. He has to do what she SAYS."
> "Not without my flashlight! I'm not scared. I'm BRAVE-scared. Brave-scared people bring a flashlight."
> "NO GIRLS ALLOWED? I'm not a girl. I'm a SISTER. That's a whole different thing."
> "It said CORRECT! You can't say ten out of ten and then SHOOT people! ...It was a GOOD trap, though."
> "Daddy's puzzle. He lets me do the three-letter ones. I always put HEN. It's right more than you'd think."

---

## How they are with each other

| | |
| --- | --- |
| **Mom and Big Sister** | Allies. Mom trusts her daughter's head, and reminds her to be gracious when she is right. |
| **Mom and Little Sister** | Mom never tells her to stop. She tells her where to aim. |
| **Big Sister and Little Sister** | They bicker like a team. One explains the plan, the other has already done it. One has three rules and the other has lodged an appeal against the third. |
| **Dad and the Son** | The same person at two sizes. Each is sure the other is the one who is lost. |
| **Mom about Dad** | She is not surprised. She is coming to get him anyway. |
| **The Son and Little Sister** | They have never compared notes, and they both think the man on the coin needs a snack. Two thousand years apart, each of them finds the sausages by smell. |

In the game they say these things to each other: click a companion to talk to her, and
look at her (right-click, or press and hold) to hear what the one you are playing thinks of her.

---

## Other people (one line each)

The format is the one from the puzzle document method: role; one trait or joke; what
they want.

**Ancient Egypt** and **Rome**

The eight people of Egypt and the seven of Rome are written out, in this form, at the
head of their own acts: [PUZZLES-egypt.md](PUZZLES-egypt.md) and
[PUZZLES-rome.md](PUZZLES-rome.md).

**The middle of Nevada, the present (draft)**

- THE OLD-TIMER: sells rocks and lemonade at the last stop before nothing, and keeps hens out back; saw the low sun flash off the wagon and the sky open where the flash fell, and has told everyone he saw nothing; wants to be asked nicely.
- THE MAN IN GRAY: stands in front of a government notice in the desert; can neither confirm nor deny the fence, a dog, or General Washington; wants nobody to read what is behind him, and is no match for a seven-year-old.

---

## For whoever draws them

Each character is a page of settings in `js/art/people.js`. Three of those settings
carry personality, and are worth as much care as the colors:

| Setting | What it is | Examples |
| --- | --- | --- |
| `stance` | How they stand when nothing is happening | Mom's clasped hands, Little Sister's fists on hips, Big Sister holding one elbow |
| `walk` | How they move | The Son bounces, Mom glides, Little Sister stomps |
| `gestures` | What their hands do when they talk | Dad shrugs, the Son throws both arms up, Big Sister raises a finger |

`tools/sprites.html` shows all of it moving.

**Colors.** Each of the family owns one color that nobody else in the family wears,
so they can be told apart at any size: Dad yellow, the Son blue with a red cap, Mom
emerald, Big Sister indigo, Little Sister pink with yellow boots. Their words on
screen are a pale tint of the same color.

---

## Big Sister's facts

Every fact she states in the game, where she says it, and how far it has been checked.
Nothing goes on this list as "Checked" from memory. The last row is somebody else's
line that rests on real history in the same way. (What the people of Egypt and Rome
say about their own times is in the tables at the end of
[PUZZLES-egypt.md](PUZZLES-egypt.md) and [PUZZLES-rome.md](PUZZLES-rome.md).)

| The fact | Line | Status |
| --- | --- | --- |
| Sliced bread was first sold on 7 July 1928, in Chillicothe, Missouri | `home.note.solve.2` (it is the password) | **Checked** |
| Atomic bombs were tested in Nevada from 1951 until 1992 | `nevada.notice.big.1` | **Checked** (first test 27 January 1951; last underground test 23 September 1992) |
| The first message sent on the network that became the internet was "LO": they were typing LOGIN and it crashed. October 1969 | `home.pc.offline.bigsis` | Headlines agree |
| Nevada became a state on 31 October 1864 | `nevada.arrive.2`; and `nevada.talk.mom.bigsis.quarter.b` ("The year Nevada became a state") | **Checked** (`us.nevada`). Abraham Lincoln, Proclamation 119, "Done at the city of Washington, this 31st day of October, A.D. 1864": https://www.presidency.ucsb.edu/node/202435 ; State of Nevada: https://jic.nv.gov/About/History_of_Nevada |
| Julius Caesar was killed on the Ides of March, 44 B.C. | `nevada.gate.2`; and `nevada.gate.2f` ("The Ides of March") | Headlines agree. (Read by the writer of the Rome act: the first row of the table in [PUZZLES-rome.md](PUZZLES-rome.md)) |
| Bartolomeo Cristofori built the first piano, in Florence, around 1700. It was called a harpsichord with soft and loud | `home.piano.look.bigsis`, `home.piano.look.bigsis2` | **Checked** (the fact-check of 7 October) |
| The coin is a Roman denarius. In 44 B.C. coins were struck in Rome with Julius Caesar's own portrait, while he was alive | `nevada.coin.read.1`, `nevada.coin.read.2`, `item.coin.bigsis` | **Checked**, through a tool that fetches a page and quotes it (see below) |
| The coin called a "penny" in Matthew 22:19 (King James Version) is, in the Greek, a denarius. The emperor then was Tiberius, so the coin brought to Jesus most likely bore his portrait | `nevada.coin.read.2c` | **Checked** (`rome.denarius.penny`). "Most likely" must stay: it may have been an older denarius, of Julius or of Augustus. https://biblehub.com/text/matthew/22-19.htm ; https://www.britannica.com/summary/Tiberius ; https://development.byustudies.byu.edu/article/coins-in-the-new-testament |
| "In God We Trust" first appeared on a United States coin in 1864, on the two-cent piece | `nevada.talk.mom.bigsis.quarter.b` | **Checked** (`us.in.god.we.trust`). "First", not "since". U.S. Mint timeline: https://www.usmint.gov/learn/history/timeline ; Law Library of Congress: https://blogs.loc.gov/law/2013/04/in-god-we-trust/ |
| A standard piano has eighty-eight keys | `home.sign.bigsis.2` (it solves Dad's riddle) | **Checked** (the fact-check of 7 October) |
| A cassette can be wound by turning its hub with a pencil | `home.tape.need.bigsis`, `item.pencil.bigsis` | **Checked** (the fact-check of 7 October), once the lines stopped giving the pencil's six sides as the reason |
| B.C. means "before Christ". A.D. is Latin: anno Domini, "in the year of the Lord" | `home.timeline.bigsis`, `home.timeline.bigsis2` | **Checked** (the fact-check of 7 October) |
| A monk named Dionysius worked out the counting of years from the birth of Jesus, in the year 525 | `home.timeline.bigsis3` | **Checked** (the fact-check of 7 October) |
| Archbishop Ussher counted the years from the Bible's own genealogies, and her timeline uses his dates | `home.timeline.1` | The author's rule (see "How the game counts the years") |
| 4004 B.C.: the Creation. 2348 B.C.: the Flood | `home.timeline.3` | The Bible's count (Ussher). The fact-check of 7 October found Ussher's own year for the Flood printed as 2349 B.C. in three sources of four and 2348 B.C. in one; the game uses the table's 2348 |
| 1921 B.C.: Abram leaves Haran, and goes down into Egypt (Genesis 12:10) | `home.timeline.5` | The Bible's count (Ussher) |
| 1491 B.C.: the Exodus | `home.timeline.6` | The Bible's count (Ussher) |
| 44 B.C.: the Ides of March | `home.timeline.6` | Rome's own date, the same in every count (see the row for `nevada.gate.2`) |
| 1921 B.C.: the year Abram went down into Egypt (Genesis 12:10). It is on her timeline | `nevada.gate.2b`; and `nevada.gate.2f` ("Abram in Egypt") | The Bible's count (Ussher), as `home.timeline.5`. Told in her own words; the verse's exact text is `kjv.gen12.10` in `briefs/out/facts-home.md` |
| From 1921 B.C. to A.D. 2026 is "nearly four thousand years" (3,946: there is no year 0) | `nevada.gate.5` ("...Nearly four thousand years early.") | The sum given in `briefs/DATING.md`, done again by `briefs/out/nevada-check.mjs` |
| John Adams and Thomas Jefferson died on the same day, 4 July 1826 | `home.talk.landing.bigsis.mom.2a` (Mom caps it: see her table) | **Checked** (the fact-check of 7 October) |
| Bombs were being tested above ground in Nevada in 1957, so a Geiger counter there had something to click at. (The old-timer says this one, not Big Sister.) | `nevada.old.after.bigsis.2` | To check |

What the words mean:

- **Checked**: read in the source named below, or in the row. "The fact-check of 7
  October" read each such fact in at least two sources, and its report (with the
  addresses) is kept with the project's working papers, not in the game; a name in
  brackets, such as `us.nevada`, is that report's own name for the item.
- **The Bible's count (Ussher)**: a year before Christ from the table in
  [How the game counts the years](#how-the-game-counts-the-years). That table is the
  author's rule for the game, and such a year is not a "fact to check" against a
  history book.
- **Headlines agree**: a web search found pages whose own titles or addresses state
  the fact. The pages were not opened, so this is weaker than Checked.
- **To check**: believed to be right, and not confirmed against anything yet.

Confirm every one that is not Checked, or change the line, before the game is called
finished.

Three lines are worded with care on purpose.

- "The network that became the internet" is the ARPANET: there were earlier
  experiments in joining two computers, so "the first message between two computers"
  would claim too much.
- The piano's first name is given as "they called it", not "he called it", because it
  is not certain the name was Cristofori's own.
- Of the coin she says only that in 44 B.C. coins were struck in Rome with Caesar's own
  portrait, while he was alive. She used to say he was "the first living Roman" on
  Rome's coins. That "first" is disputed (the page read for it says "living Romans had
  appeared on coinage before", and counts his as "the third instance"), so it is gone.

Sources for the three that are checked:

- Wikipedia, [Otto Frederick Rohwedder](https://en.wikipedia.org/wiki/Otto_Frederick_Rohwedder): his bread-slicing machine was first used commercially by the Chillicothe Baking Company of Chillicothe, Missouri, on 7 July 1928.
- Wikipedia, [Nevada Test Site](https://en.wikipedia.org/wiki/Nevada_Test_Site): nuclear testing there began on 27 January 1951, and the last underground test was on 23 September 1992.
- The coin, read on 2026-10-07 through a tool that fetches a page and reports on it with quotations, which is one step short of reading the page oneself. Wikipedia, [Roman currency](https://en.wikipedia.org/wiki/Roman_currency): "Julius Caesar issued coins bearing his own portrait"; "The appearance of Caesar's portrait on Roman denarii in 44 BC"; "Caesar's coinage marked the third instance in Roman history where a living individual was depicted". Leu Numismatik, [The earliest portrait denarius of Julius Caesar](https://leunumismatik.com/en/lot/44/158): a denarius with the "wreathed head of Julius Caesar", struck at "Rome, January 44" by the moneyer M. Mettius.

Pages whose headlines agree with the next three:

- "LO": Paleofuture, [The First Internet Message Ever Sent Was "LO"](https://paleofuture.com/blog/2014/7/3/the-first-internet-message-ever-sent-was-lo); History of Information, [Charley Kline Sends the First Message Over the ARPANET](https://www.historyofinformation.com/detail.php?entryid=1108); This Day in Tech History, 29 October, [First Message on the Internet](https://thisdayintechhistory.com/10/29/first-message-on-the-internet/).
- Nevada, before it was checked (its row now names the sources read): History.com, This Day in History for 31 October, [the U.S. Congress admits Nevada as the 36th state](https://www.history.com/this-day-in-history/october-31/the-u-s-congress-admits-nevada-as-the-36th-state).
- The Ides of March: JURIST, [Julius Caesar assassinated on Ides of March](https://www.jurist.org/news/page/6531); History.com, This Day in History for 15 March, [The Ides of March](https://www.history.com/this-day-in-history/march-15/the-ides-of-march).

---

## Mom's facts

Every fact Mom states in the game ("A matter of record:"), and where she says it. The
same rule as for her daughter: every one is true, and nothing goes on this list as
"Checked" from memory. The three words mean what they mean in Big Sister's table.

| The fact | Line | Status |
| --- | --- | --- |
| A full-size piano has eighty-eight keys | `home.sign.mom.2` (it solves Dad's riddle) | **Checked** (the fact-check of 7 October) |
| The Constitution of the United States begins "We the People", and was signed in Philadelphia on 17 September 1787 | `home.frame.mom`, `home.vault.right.1` (1787 is the family vault's combination) | **Checked** (the fact-check of 7 October) |
| The Declaration of Independence was adopted on 4 July 1776 | `home.vault.wrong.1776` | **Checked** (the fact-check of 7 October) |
| The government under the Constitution began in 1789, and George Washington took the oath as President that year | `home.vault.wrong.1789` | **Checked** (the fact-check of 7 October) |
| In March 1776 Abigail Adams wrote to John Adams, "Remember the Ladies" | `home.shelf.mom2` | **Checked** (the fact-check of 7 October) |
| As a schoolboy George Washington copied out 110 Rules of Civility | `home.talk.landing.mom.bigsis.1a` | **Checked** (the fact-check of 7 October) |
| John Adams and Thomas Jefferson died fifty years to the day after the Declaration | `home.talk.landing.bigsis.mom.2b` (Big Sister gives the date: 4 July 1826) | **Checked** (the fact-check of 7 October) |
| Martin Luther wrote the hymn "A Mighty Fortress Is Our God" | `home.piano.use.mom` | **Checked** (the fact-check of 7 October) |
| Psalm 46 is the psalm behind that hymn | `home.piano.use.mom2` | To check (the fact-check confirmed the verse's words and the hymn's author; that the hymn is drawn from this psalm is the common account) |
| Johann Sebastian Bach wrote "S.D.G." at the end of many of his scores: Soli Deo Gloria, "to God alone the glory" | `home.talk.study.mom.bigsis.1a` | **Checked** (the fact-check of 7 October) |
| A cassette's tape is wound back in with a pencil in its hub | `home.tape.wind.1` (she does it) | **Checked** (the fact-check of 7 October) |
| Archbishop Ussher's book of dates (his Annals) was published in 1650 | `home.timeline.2` | To check. It is the year the author's rule gives ("his Annals, 1650") |
| The tune the Retreat's sound machine plays is in D major | `home.sound.look.mom`, `home.talk.retreat.mom.bigsis.key.a` | True of the game's own track (`retreat` in js/content/sound.js: five notes of D major) |
| The thirty-first of October is Reformation Day: Martin Luther's Ninety-five Theses are dated 31 October 1517 | `nevada.arrive.2b` (she caps her daughter's "Halloween") | **Checked** (`us.reformation.day`). Never "to the very day": Luther's date is in the old calendar. https://www.britannica.com/print/article/415676 |
| By the time he was sixteen George Washington had copied out 110 Rules of Civility | `nevada.agent.mom.5` (said to the man in gray, on her second try) | **Checked** (`us.washington.rules`). He copied them; he did not write them. https://blogs.loc.gov/teachers/2012/05/george-washington-living-the-rules-of-civility/ ; https://www.mountvernon.org/library/digitalhistory/digital-encyclopedia/article/the-rules-of-civility-and-decent-behaviour |
| When the Constitution was signed, Benjamin Franklin said of the sun on the back of Washington's chair that it was "a rising and not a setting Sun" | `nevada.flash.sun` (only when it is Mom who holds the coin up) | **Checked** (`us.franklin.sun`). The seven words are James Madison's record of him, 17 September 1787, capital S and full stop included. The chair's sun is carved (National Park Service); Madison's word was "painted", so "carved" stays outside the quotation marks. https://avalon.law.yale.edu/18th_century/debates_917.asp ; https://www.nps.gov/articles/000/assembly-room-furnishings.htm |
| Julius Caesar's coins bore his own portrait; American money bears the motto "In God We Trust" | `nevada.talk.mom.bigsis.quarter.a` | **Checked**: the portrait as in Big Sister's table (the coin); the motto `us.in.god.we.trust` (its sources are in Big Sister's table). She does not say whose face is on the quarter: "on the quarter since 1932" is no longer true of every quarter (`us.quarter`). |
| B.C. means "before Christ" | `nevada.gate.2d` (she tells Little Sister) | **Checked** (`time.bc.ad`). https://www.britannica.com/topic/Christian-Era |
| Genesis 12 is the chapter in which Abram goes down into Egypt | `nevada.gate.2e` ("Genesis 12. I have known that chapter all my life, darling.") | **Checked** (`kjv.gen12.10`): https://biblehub.com/kjv/genesis/12-10.htm ; https://www.bibleserver.com/KJV/Genesis12 . She names the chapter and quotes nothing of it. |

Four are worded with care on purpose.

- Of the piano, "a full-size piano" (and Big Sister says "a standard piano"): a few
  pianos have more keys than eighty-eight, or fewer.
- Of Bach, "many of his scores": not all of them.
- Of the cassette, neither of them says that the pencil's six sides are why it fits.
  The fact-checker found pages that say a pencil fits the hub, and none that give the
  six sides as the reason. (Dad's pencil is six-sided in the picture, and that is fine.)
- Of the sun on General Washington's chair she says "carved", which is right for the chair,
  and quotes only Dr. Franklin's seven words. James Madison, who wrote them down, called
  the sun "painted".

## Scripture quoted in the game

King James Version, exact, with the reference said in the same line. Listed here so
that each can be checked word for word, capitals and punctuation included.

| Verse | The words quoted | Line | Who says it, and where | Status |
| --- | --- | --- | --- | --- |
| Psalm 121:1 | "I will lift up mine eyes unto the hills, from whence cometh my help." | `home.bible.bigsis` | Big Sister, at the family Bible | **Checked** (the fact-check of 7 October) |
| Psalm 121:2 | "My help cometh from the LORD, which made heaven and earth." | `home.bible.mom` | Mom, at the family Bible | **Checked** (the fact-check of 7 October) |
| Psalm 23:1 | "The LORD is my shepherd; I shall not want." | `home.bible.lilsis` | Little Sister, at the family Bible, by heart | **Checked** (the fact-check of 7 October) |
| Psalm 121:8 | "The LORD shall preserve thy going out and thy coming in from this time forth, and even for evermore." | `home.door.psalm.3` (the reference is Big Sister's line before it, `home.door.psalm.2`) | Little Sister, at the front door, before they leave | **Checked** (the fact-check of 7 October) |
| Joshua 24:15, its last clause | "...as for me and my house, we will serve the LORD." | `home.sampler.mom` | Mom, at the sampler over the front door | **Checked** (the fact-check of 7 October) |
| Psalm 46:1 | "God is our refuge and strength, a very present help in trouble." | `home.piano.use.mom2` | Mom, at the piano, after the hymn | **Checked** (the fact-check of 7 October) |
| Matthew 23:37, nine words from the middle of the verse | "even as a hen gathereth her chickens under her wings" | `home.nest.mom` | Mom, at the nest in Little Sister's room. (No full stop inside the quotation marks: the verse goes on.) | Given as exact King James in the editor's brief; to check against a printed text |
| Matthew 22:21, its second sentence | "Render therefore unto Caesar the things which are Caesar's; and unto God the things that are God's." | `nevada.coin.read.2d` (the reference, "Matthew 22:21.", is in the same line) | Mom, when Big Sister reads the coin, in Nevada | **Checked** (`kjv.matt22.19-21`): https://www.bibleserver.com/KJV/Matthew22 ; https://biblehub.com/kjv/matthew/22.htm |
| Psalm 31:15, its first clause | "My times are in thy hand" | `nevada.gate.5b` (the reference, "Psalm 31, verse 15.", is in the same line) | Mom, at the end of Act Four, the second line after "Daddy's EARLY" | **Checked** (`kjv.ps31.15`): https://biblehub.com/kjv/psalms/31-15.htm ; https://www.bibleserver.com/KJV/Psalm31 . The clause is followed by a colon in the King James text, so the quotation marks close before the line's own colon and there is no full stop inside them. |

Told and not quoted: Genesis 12:10 (Abram goes down into Egypt: `home.timeline.5` and
`nevada.gate.2b`, in Big Sister's own words; in Act Four her mother names the chapter,
`nevada.gate.2e`, and quotes nothing of it).
Named and not quoted: the hymn "A Mighty Fortress Is Our God" (`home.piano.use.mom`); and
the hymn "O God, Our Help in Ages Past" (`nevada.talk.lilsis.mom.3b`: Mom is humming it
in Nevada; the title is to confirm, under "To confirm" at the end of
[PUZZLES-the-present.md](PUZZLES-the-present.md)).
Quoted from documents, not from Scripture: "We the People" (the first three words of
the Constitution), "Remember the Ladies" (three words of Abigail Adams's letter),
"a rising and not a setting Sun." (seven words of Benjamin Franklin's, as James Madison
recorded them at the signing of the Constitution: `nevada.flash.sun`) and "In God We
Trust" (the motto: `nevada.talk.mom.bigsis.quarter.a`).
