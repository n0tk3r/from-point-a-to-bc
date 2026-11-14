# How the game talks, and how its puzzles play fair

<!-- WRITE-25: round twenty-five. The author, 13 November: "The dialogue that has been produced is very strange. I need you
to study what dialogues in LucasArts games, Sierra games (especially King's Quest 6 and Gabriel Knight, Jane Jensen written
dialogue) looks like and do better with generating character dialogue. Also develop the puzzles more, on the ship the dial
was impossible to solve, the characters kept saying they needed to sound something but there was no way of knowing how to
say it out loud for the person steering the ship". His answers: what felt strange was all four things measured below; a
narrator for looks, as Sierra's games have; a pilot on the ship first; the puzzles fair, and richer too. -->

This is the guide every line and every puzzle is written to from round twenty-five on. It replaces the rules for lines in
`CHARACTERS.md` ("Rules for every line") wherever they disagree; the characters' pages there still say who each person is.
The ship (Act Six's deck, its compass and its two cut-scenes) is the first stretch written to it; the rest of the game
follows once the author has played the ship.

## 1. What the classics do

### Gabriel Knight: Sins of the Fathers (Jane Jensen, Sierra, 1993)

Measured from a transcript of the game's lines:

- **Short, whole sentences.** Gabriel and Grace average about seven words a line; three lines in four are complete
  sentences. They contract, always.
- **About half the lines are plain.** "Good luck." "He left for the day." Only about half try to be funny, and the jokes
  land because the plain lines around them let them.
- **Jokes come from who is talking.** Gabriel's money troubles and failed novels, Grace's competence and her opinion of
  his habits. Banter is a setup, a deflation, a comeback: he boasts, she flattens it, he answers. A line nearly always
  tells you who is speaking and what they want.
- **A narrator describes things**, in the third person, about eleven words at a time: first a plain fact about the thing,
  then a remark that says something about Gabriel or his situation. About half its descriptions carry a wry aside; the
  rest are just good description.
- **Emphasis is rare.** A word in capitals in about one line in forty; an ellipsis for a trail-off in the middle of a
  line, almost never to open one.
- **The menu is the to-do list.** The topics you can ask about are the leads you have. Jensen breaks a mystery into
  "little pieces of information" and decides when and how the player gets each one.
- **Story first.** Each day of the game begins with banter at the shop, then the errands; nobody leaves a chapter stuck,
  because the chapter does not end until everything in it is done.

### King's Quest VI (Roberta Williams and Jane Jensen, Sierra, 1992)

- **A narrator reports what the hero does**; the characters speak for themselves only when they are talked to.
- **Each character is built on one clear trait**: the gruff ferryman, the fair-minded pawnbroker, the sad clown, the
  cranky stick-in-the-mud. They talk from that trait every time.
- **The official hint book grades every question**, from a playful nudge, to a narrowing clue (the place, the person, the
  kind of thing), to the exact action. Its own advice to players: an error message can tell you what will work.
- **Mercy in the design**: far fewer ways to get stuck than the game before it; some puzzles with more than one solution;
  a shorter and a longer road to the end.

### The Monkey Island games (Ron Gilbert, Dave Grossman, Tim Schafer, LucasArts, 1990 and 1991)

- **Funny from character and situation**, not from one-liners: the team was told to be funny "the way The Simpsons is
  funny", and each person has a comic engine (a salesman's patter, a squabbling pair, a bureaucracy that upgrades its
  door every time you escape).
- **Read aloud, rewritten until it got a laugh.** Dialogue was tried on colleagues and rewritten when it did not land.
- **The obvious solution fails, funnily, and points at the real one** (Schafer's example: the hammer that turns out to be
  rubber). Being stuck has to be entertaining, and the replies to wrong tries are where the hints live.
- **Setups pay off** (a boast early on, needed much later), and the player is never punished for choosing the funny line.

### Ron Gilbert's rules (1989)

The end goal is clear from the start; the next step is always known; no puzzle is solved before its problem is seen; a
puzzle's answer makes the player say "of course", not "I'd never have got that"; when the player has the right idea,
the game lets it work (reward intent); nothing happens because of an unrelated action; every puzzle moves the story on;
and the player always has more than one thing they can be doing.

## 2. What was wrong with ours

Measured over every line of the game in round twenty-four:

| | Our lines | Gabriel Knight |
| --- | --- | --- |
| Words in a family member's line | 10 to 13 | about 7 |
| Lines trying to be funny | nearly all | about half |
| Little Sister's lines with a word in capitals | 81% | about 2% |
| The Son's | 20% | |
| Mom's lines with "darling" or "sweetheart" | 16% | |
| Little Sister's lines of three or more clipped sentences under 16 words | 46% | |
| Big Sister's | 24% | |
| Other people's lines that open with "..." | 14% (Japan) to 21% (elsewhere) | almost none |

What that adds up to, in the author's words "very strange":

- **Every line is a quip**, and many are slogans that could be said by anyone about anything ("I regret nothing.").
- **Choppy, stiff sentences**: the three-beat pattern everywhere ("I knocked. It sounds hollow. It's meant to, I
  suspect."), and Big Sister refusing things in full words ("I am not opening a cask at sea.").
- **Reports of what someone just did**, in the past tense, for every try ("I went to the bow. I came back damp."). That is
  a narrator's job; in our mouths it reads like a log.
- **The crew talk in broken fragments** ("...Can't see the card. ...Sun's on it."). People who are speaking their own
  language should sound fluent.
- **Tics instead of voices**: a capital word in almost every line of Little Sister's, "darling" every few lines of Mom's,
  "I am writing that down" over and over.
- **Puzzle mechanics said as instructions** ("Now I have to say it so the helm can hear it."), which on the ship pointed
  the player the wrong way.

## 3. Who says what

### The narrator

New in round twenty-five (the engine's speaker `narrator`: a caption in a book face along the bottom of the picture, no
figure, nobody's mouth moving). The narrator answers **Look at** and **Use** (tries), and the stock replies; the family
answers when someone talks to them, when they talk to each other, and at the moments of the story.

- **Third person, present tense.** The lead is named by role, "Mom", "Big Sister", "Little Sister", then "she".
- **A plain description first**: what it is, specifically enough that the player can find it in the picture. Then, often,
  one more sentence: what it means, who it belongs to, how someone feels about it.
- **One or two sentences, 8 to 25 words.** About one description in three has a joke in it. The rest are simply good.
- **Tries say what happens, or why not**, naming the lead. A near miss says what is missing: this is where the hints live.
- **Warm.** It never mocks the family; it enjoys them. No capitals for emphasis, no exclamation marks, no "..." to open,
  no "you".
- **One line for all three** unless who is trying changes the answer (Little Sister cannot reach it; Mom has a reason;
  Big Sister knows a fact).

### The family

They speak in conversations, to each other, in the hints, and at the story's moments.

- **Contractions always**, Big Sister included: she is thirteen. Her precision is in her word choice, not in "I am not".
- **Whole sentences, varied in length**, broken only where people really break off. Read it aloud: if no person would say
  it like that, it is rewritten.
- **About half the lines plain.** The joke, when there is one, is that person's way of seeing the thing.
- **Tics are seasoning, not voices**: Little Sister's capital word in at most one line in five, never twice in a row;
  Mom's "darling" or "sweetheart" at most once a conversation, and only to her girls; Big Sister's fact when it matters,
  "I'm writing that down" once an act.
- **No reports.** Nobody narrates what they just did; the narrator does.

### The other leads, and the people of the past

Round twenty-five's second half (the whole game, 13 November) adds the leads the ship does not have. The narrator names
them as it names the girls: "Dad", "the Son", "Grandpa Joe", "Ranger".

- **Dad**: cheerful, stubborn, certain, a little wrong. His joke is the pun and the confident mistake, in at most one line
  in five; the rest is a father looking for his boy, which he never says outright. Whole sentences, contracted.
- **The Son**: ten, loud, thrilled by everything, and missing his dad under the noise. Kid logic and enthusiasm, not
  slogans; a word in capitals in at most one line in ten.
- **Grandpa Joe**: an old man of the desert road, slow, dry and kind, a storyteller. His way of talking ("ain't", a dropped
  "g", "partner") is seasoning, a word or two a line at most, never spelled out phonetically.
- **Ranger** never speaks: his line stays "..." (or "...!") with his pictures. The narrator does his looks and tries
  ("Ranger sniffs the button and decides it is not food.").
- **The people of Egypt and Rome** speak in whole words, without contractions, which sets them in their own time; but in
  natural, flowing sentences, never broken and never opening on "...". Everyone else follows "Everyone else", below.

### Everyone else

- **They speak their own language, so they sound fluent**: complete sentences, the words of their trade and their place,
  no dropped words, no pidgin, nothing opening with "...". The few words of their own (a ship's "etekō") are glossed once.
- **One want and one way of talking each.** The ship: Kanbei proud and gruff, hiding his eyes; Denzō huge, warm and
  superstitious, who talks more than anyone; Kōta twelve, shy, homesick and eager; Gonroku a captain who talks about the
  weather; Seijirō, who counts everything.
- **They answer the question they are asked**, in character, and say a clue plainly.

## 4. The numbers a stretch is checked against

| | Limit |
| --- | --- |
| A family member's line | 4 to 18 words, most 6 to 12 (a quick "No." or "And?" in an exchange aside) |
| The narrator's line | 8 to 25 words |
| A box | 115 characters spoken (as the other acts since round twenty-two), 150 the narrator's |
| Lines with no joke in them | at least two in five |
| Little Sister's lines with a word in capitals | at most one in five |
| The Son's | at most one in ten |
| Anyone else's | at most one in fifty (a sign or a label as written aside) |
| Dad's puns | at most one line in five |
| Lines opening with "..." | none |
| Exclamation marks | the children one line in ten at most; grown-ups rarely |
| Lines of three or more clipped sentences under 16 words | one in ten at most |

## 5. Puzzles: fair, and richer

1. **The goal is said in the scene**, plainly, by someone who wants it done ("Kanbei, the heading!").
2. **The next step is always visible.** After each success something changes, and someone or the narrator says what is
   next, or it is in plain sight.
3. **The obvious try fails in a way that teaches** and is funny: it points at the real answer.
4. **Every wrong try is answered specifically**, and a near miss says what is missing.
5. **Reward intent.** The way a player would naturally try it works: clicking the mark the needle is on lets her call it;
   showing Kōta the pennies starts the trade.
6. **No unconnected events.** Every requirement has a reason that someone in the scene can say.
7. **Hints climb one rung per stage**: the goal, then who or where, then what, then the exact action; spoken by the lead
   in her own words.
8. **Richer**: a puzzle uses more than one of the family's talents; a twist that is funny and teaches something true; a
   small physical step where it is natural; and, where it fits, a second road to the answer.
9. **True to history.** A custom used in a puzzle is checked before it goes in (Big Sister's facts, `CHARACTERS.md`).

## 6. Before and after (the ship)

| Before | After |
| --- | --- |
| Big Sister: "I knocked. It sounds hollow. It's meant to, I suspect." | Narrator: "Big Sister knocks on the mast step. It sounds hollow." |
| Big Sister: "I went to the bow. I came back damp. I regret nothing." | Narrator: "Big Sister makes it as far as the bow, gets thoroughly splashed, and comes back pleased with herself." |
| Little Sister: "I pushed a bar. It didn't go. The sailor laughed. NICELY." | Narrator: "Little Sister pushes a windlass bar with all her might. The nearest sailor grins at her." |
| Kanbei: "...Can't see the card. ...Sun's on it." | Kanbei: "Give me a moment, Captain. The sun's sitting right on the card." |
| Gonroku (after "Monkey!"): "Say it so the helm can hear it." | Denzō: "Don't say that word! Not on a ship." |
| Big Sister: "A polite word for everything one must not say. That is very well organized." | Kōta, plainly, to the one he talks to: "At sea that one is etekō. Only ever etekō. The other word makes the lady leave." |

The ship, measured the same way as section 2, before and after (the deck, the compass, the ship's people, Casting Off, the
Uttermost Parts' lines, the ship's hints and things):

| | Before | After |
| --- | --- | --- |
| Lines | 537, none the narrator's | 448, 147 of them the narrator's |
| Words in a family member's line | 11.2 | 8.9 |
| Little Sister's lines with a word in capitals | 84% | 5% |
| Mom's lines with "darling" or "sweetheart" | 11% | 2% |
| Three or more clipped sentences (Little Sister / Big Sister) | 50% / 31% | none |
| The crew's lines that open with "..." | 24% | none |
| The family reporting what they just did ("I knocked...") | 17 | none |

## 7. Sources

- Hardcore Gaming 101, "King's Quest VI: Heir Today, Gone Tomorrow" (Kurt Kalata, 2019):
  https://www.hardcoregaming101.net/kings-quest-vi-heir-today-gone-tomorrow/
- The Digital Antiquarian (Jimmy Maher), on King's Quest VI: https://www.filfre.net/2019/07/05/
- The official King's Quest VI hint book: https://mocagh.org/sierra/kq6-hintbook.pdf
- Game Developer, "Hunting Shadows: The Making of Gabriel Knight":
  https://www.gamedeveloper.com/design/hunting-shadows-the-making-of-gabriel-knight
- The Escapist, "The Escapist Interview: Jane Jensen": https://www.escapistmagazine.com/the-escapist-interview-jane-jensen/
- Gabriel Knight 20th Anniversary transcript (Gabriel Knight wiki): https://gabrielknight.fandom.com/wiki/GK1HD_transcript
- USgamer, Tim Schafer interview: https://www.usgamer.net/articles/Tim_Schafer_Interview?page=2
- Vice, "Tim Schafer Discusses His Classic Video Games": https://vice.com/en/article/tim-schafer-discusses-grim-fandango-and-monkey-island-990
- Spillhistorie, "A conversation with Dave Grossman" (2025): https://spillhistorie.no/2025/05/23/a-conversation-with-dave-grossman/
- The Digital Antiquarian, on Day of the Tentacle: https://www.filfre.net/?p=3960
- Ron Gilbert, "Why Adventure Games Suck" (1989): https://grumpygamer.com/why_adventure_games_suck
- Japan's sea customs used on the ship: the Funadama (female; enshrined in the mast; paper dolls, two dice, twelve coins,
  a woman's hair, grain sealed in; words she dislikes, among them monkey and cat, not said aboard; a small bell-like sound,
  "Funadama-sama ga isamu", a good sign) as recorded village by village in Gabi Greve's compilation,
  https://japanshrinestemples.blogspot.com/2017/09/funadama-funatama-boat-deity.html ; "etekō" for the monkey, a
  rewording that avoids "saru" (which sounds like 去る, to leave): https://dic.pixiv.net/a/%E7%8C%BF
