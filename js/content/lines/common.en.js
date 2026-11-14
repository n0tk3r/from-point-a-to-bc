// Lines that belong to no one act: the opening movie, what the family say when they look at one another or hand
// something over, and the stock replies for things nobody wrote a line for.
//   "line.id": ["who", "What they say."]
// PASS-17E (round seventeen, the dialogue pass): five lines have new words under their old ids, each marked with why
// (Mom's stock replies talk to her girls as a mother does, with her contractions; Big Sister's look at her mother is
// said in the morning too). Ranger's and Grandpa Joe's stock lines are as they were: the Office's are WRITE-17's.
// PASS-19E (round nineteen, 25 October: the author's "Stiff, written-sounding", "Too long", "Jokes fall flat"): four
// lines have new words under their old ids (S/work-19-passE/changes.json): one exclamation a box, no name as address.

export const lines = {
  // ---------- intro movie ----------
  "intro.1": ["son", "Dad, the road stops on the map. There's just a little drawing of a shrug."],
  "intro.2": ["dad", "Maps don't know about shortcuts."],
  "intro.3": ["son", "Dad. Dad! The sky's doing the thing my slushie does."],
  "intro.4": ["dad", "That's weather. Probably."],
  "intro.5": ["son", "Are we when yet?"],
  "intro.6": ["dad", "No, but we're making good time."],


  // ---------- the sketch example scene ----------
  "sketch.stall": ["son", "Placeholder fruit. It tastes like a to-do list."],
  "sketch.gate": ["son", "This gate isn't drawn yet. Nine out of ten, for a rectangle."],
  "sketch.cart": ["son", "A cart, according to the label."],
  "sketch.cart.use": ["son", "I'd push it, but it's mostly a rectangle."],


  // ---------- looking at each other ----------
  "see.mom.bigsis": ["narrator", "Big Sister, thirteen, with a fact ready for every occasion. Mom trusts that head of hers more than most maps."],
  "see.mom.lilsis": ["narrator", "Little Sister, seven years old and built without brakes. Mom wouldn't change a thing."],
  "see.bigsis.mom": ["narrator", "Mom hasn't raised her voice once since Dad went missing. That's how Big Sister knows it's serious."],  // PASS-17E: continuity (it is said in the morning in Nevada too)
  "see.bigsis.lilsis": ["narrator", "Little Sister: small, loud and occasionally useful. Big Sister would rather she didn't hear the last part."],
  "see.lilsis.mom": ["narrator", "Mom, who smells like the good soap. Little Sister likes to keep her where she can see her."],
  "see.lilsis.bigsis": ["narrator", "Big Sister knows everything, which Little Sister finds very annoying and very handy."],
  // NEVADA-12W: Grandpa Joe and Ranger, the team of two in Act Five
  "see.grandpajoe.ranger": ["narrator", "Ranger, Grandpa Joe's partner. He doesn't say much, and Joe can't recall him ever being wrong."],
  "see.ranger.grandpajoe": ["narrator", "Grandpa Joe, seen from knee height. As far as Ranger is concerned, he's the best thing in the desert."],


  // ---------- handing something over ----------
  "give.dad.1": ["dad", "Here you go, buddy. Don't lose it before I do."],
  "give.son.1": ["son", "Here, catch. It's a hot potato, except it isn't a potato."],
  "give.mom.1": ["mom", "Would you hold on to this for me?"],
  "give.bigsis.1": ["bigsis", "Here, you take it. Tell me what you find out."],
  "give.lilsis.1": ["lilsis", "Can you hold this? It's very important."],
  "give.grandpajoe.1": ["grandpajoe", "Here, partner. Keep hold of that for me."],                      // NEVADA-12W
  "give.ranger.1": ["ranger", "..."],                                                            // NEVADA-12W


  // ---------- nothing to suggest ----------

  // ---------- stock replies ----------
  "nope.dad.1": ["narrator", "Dad considers it, and decides that isn't how he'd do it."],
  "nope.dad.2": ["narrator", "It doesn't work. Dad respects the idea all the same."],
  "nope.dad.3": ["narrator", "That gets Dad nowhere, and he has read half a manual."],
  "nope.son.1": ["narrator", "The Son tries it in his head first. It doesn't work in there either."],
  "nope.son.2": ["narrator", "Nothing happens. The Son gives the idea zero out of ten."],
  "nope.son.3": ["narrator", "It's a bad plan, and not one of the Son's good bad plans."],
  "nope.mom.1": ["narrator", "Mom thinks it over and decides that won't do."],  // PASS-17E: Mom's formality
  "nope.mom.2": ["narrator", "That won't work. Mom would rather try something Dad wouldn't."],  // PASS-17E: Mom's formality; funnier ("your father", with fond exasperation)
  "nope.mom.3": ["narrator", "It's a creative idea. Mom sets it gently to one side."],
  "nope.bigsis.1": ["narrator", "Big Sister can think of three reasons that won't work, in order."],
  "nope.bigsis.2": ["narrator", "Nothing comes of it. Big Sister isn't surprised: historically, nothing ever has."],
  "nope.bigsis.3": ["narrator", "Big Sister decides against it. Some ideas are better left as footnotes."],
  "nope.lilsis.1": ["narrator", "Little Sister gives it a good try, and it doesn't go."],
  "nope.lilsis.2": ["narrator", "Little Sister thinks that's silly, and she knows silly when she sees it."],
  "nope.lilsis.3": ["narrator", "That doesn't work. Little Sister wonders whether trying earns a snack."],
  "look.dad.1": ["narrator", "There's nothing here to write home about, and Dad writes home about nearly everything."],
  "look.son.1": ["narrator", "It's just a thing. The Son stares at it until he's sure he has won."],
  "look.mom.1": ["narrator", "Nothing here needs Mom's attention, which makes a restful change."],
  "look.bigsis.1": ["narrator", "There's nothing remarkable about it. Big Sister takes note of it anyway."],
  "look.lilsis.1": ["narrator", "It's only a thing, and Little Sister has more interesting things to look at."],
  "hint.dad.none": ["dad", "I'm out of ideas. I'll look around and call that the plan."],  // PASS-17E: funnier
  "hint.son.none": ["son", "No idea. I'll poke things until something happens, like a scientist."],
  "hint.mom.none": ["mom", "I haven't the faintest idea. Let's have a proper look around."],  // PASS-17E: Mom's formality
  "hint.bigsis.none": ["bigsis", "I don't know yet. That doesn't happen often, so let's look around."],
  "hint.lilsis.none": ["lilsis", "I don't know. Let's ask somebody tall."],
  // NEVADA-12W: Grandpa Joe's stock lines, and Ranger's (his are dots, and nobody translates a stock line)
  "nope.grandpajoe.1": ["narrator", "Grandpa Joe has been around long enough to know a thing that won't work. This is one."],
  "nope.grandpajoe.2": ["narrator", "Grandpa Joe shakes his head, kindly. That one's a no."],
  "nope.grandpajoe.3": ["narrator", "Grandpa Joe thinks on it for a good while, and then decides against it."],
  "nope.ranger.1": ["narrator", "Ranger sniffs at the idea and decides it isn't food."],
  "nope.ranger.2": ["narrator", "Ranger gives it a long, careful look and leaves it alone."],
  "nope.ranger.3": ["narrator", "Ranger tries it with both paws. Nothing happens, and he looks offended."],
  "look.grandpajoe.1": ["narrator", "It isn't much, but it's there. Grandpa Joe has made do with less."],
  "look.ranger.1": ["narrator", "Ranger looks it over and finds nothing worth washing."],
  "hint.grandpajoe.none": ["grandpajoe", "I ain't got a notion yet. Let's look around, slow and proper."],
  "hint.ranger.none": ["ranger", "..."],
  // ---- TALK-24: the way back out of a topic in a talk (js/content/talk/topics.js), said by whoever is being played ----
  "talk.back.mom": ["mom", "Let me ask about something else."],
  "talk.back.bigsis": ["bigsis", "Can I ask about something else?"],          // WRITE-25: as she talks now (docs/WRITING.md)
  "talk.back.lilsis": ["lilsis", "I want to ask a different thing."],          // WRITE-25: no capital word on the way back
  "talk.back.son": ["son", "Wait, I've got a different question."],
  "talk.back.dad": ["dad", "Let me ask you something else."],
  "talk.back.grandpajoe": ["grandpajoe", "Let's talk about something else, partner."],
  "talk.back.ranger": ["ranger", "..."],
};
