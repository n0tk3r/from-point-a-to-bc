// Every spoken line in the game, in English.
//   "line.id": ["who", "What they say."]
// Scripts refer to lines by ID only. A voice recording for a line is a sound file
// named after its ID (see js/content/sound.js). A translation is a copy of this
// file with the same IDs.
//
// PLACEHOLDER CONTENT below, written to prove the engine. All of it is original.

export const lines = {
  // ---------- intro movie ----------
  "intro.1": ["son", "Dad, the map says this road ends."],
  "intro.2": ["dad", "Maps don't know about shortcuts."],
  "intro.3": ["son", "Why is the sky swirling?"],
  "intro.4": ["dad", "Weather. Probably."],
  "intro.5": ["son", "Are we when yet?"],
  "intro.6": ["dad", "No, but we're making good time."],

  // ---------- Egypt: Dad ----------
  "egypt.arrive.1": ["dad", "Okay. Nobody panic. The car has landed."],
  "egypt.arrive.2": ["dad", "Buddy? ... Buddy?"],
  "egypt.arrive.3": ["dad", "He was in the passenger seat a minute ago. Or a thousand years from now. I'm still working out the tenses."],
  "egypt.wagon.look": ["dad", "Two hundred thousand miles and she still runs. Not right now. But in general."],
  "egypt.wagon.use": ["dad", "There's a road map in the glovebox. Three states, zero centuries."],
  "egypt.wagon.empty": ["dad", "Nothing left in there but ketchup packets. I'm saving those."],
  "egypt.river.look": ["dad", "Either that's the Nile or a very committed car wash."],
  "egypt.reeds.look": ["dad", "Reeds. Nature's ballpoint."],
  "egypt.reeds.take": ["dad", "One reed. I'll bring it back. That's a lie. I never bring pens back."],
  "egypt.reeds.again": ["dad", "One is plenty. I'm not opening a stationery shop."],
  "egypt.pyramids.look": ["dad", "They look brand new. Somebody kept the receipt."],
  "egypt.scribe.look": ["dad", "He's been staring at a blank sheet for a while. I know writer's block when I see it."],
  "egypt.scribe.hello": ["scribe", "You fell out of the sky in a red chariot with no horses."],
  "egypt.scribe.hello2": ["dad", "It has a hundred and forty horses. They're resting."],
  "egypt.ask.boy": ["dad", "Have you seen a boy? About this tall, asks a lot of questions?"],
  "egypt.ans.boy": ["scribe", "A small one fell from the sky before you did. The humming door took him away again."],
  "egypt.ans.boy2": ["scribe", "I would write down where it went. But my pen is at the bottom of the river."],
  "egypt.ask.door": ["dad", "What is the humming door?"],
  "egypt.ans.door": ["scribe", "It opens by the water. It closes when you look at it too hopefully."],
  "egypt.ask.bye": ["dad", "I'll let you get back to your sheet."],
  "egypt.ans.bye": ["scribe", "It is not going anywhere. Neither am I."],
  "egypt.give.reed": ["dad", "Here. It's a pen. Some assembly required."],
  "egypt.got.reed": ["scribe", "A good reed. You have the eye of a scribe and the clothes of a market stall."],
  "egypt.need.sheet": ["scribe", "Now I need something to draw the door's path on. This sheet is for taxes."],
  "egypt.give.map": ["dad", "Draw on this. It's a map. It's already wrong, you can't make it worse."],
  "egypt.got.map.nopen": ["scribe", "A fine sheet. I have nothing to mark it with."],
  "egypt.got.map": ["scribe", "There. The door opens here, then here, then here. It likes a schedule."],
  "egypt.door.steady": ["scribe", "Stand where I have marked and it will hold still for you."],
  "egypt.hole.look": ["dad", "A hole in the air the size of a dinner plate. I am not the size of a dinner plate."],
  "egypt.hole.small": ["dad", "It shrinks every time I get close. I have the same effect on waiters."],
  "egypt.hole.big": ["dad", "Now that's a door."],
  "egypt.hole.go": ["dad", "Hold on, buddy. Dad's taking the next shortcut."],
  "egypt.hole.wait": ["dad", "Not until I know where it comes out. I've made that mistake once today."],

  // ---------- Rome: Son ----------
  "rome.arrive.1": ["son", "Dad? This isn't the rest stop."],
  "rome.arrive.2": ["son", "Everyone here is wearing a bedsheet. Either this is Rome or a very big sleepover."],
  "rome.temple.look": ["son", "Columns. Dad would say they're holding up well."],
  "rome.fountain.look": ["son", "There are coins at the bottom. People have been wishing here for a while."],
  "rome.fountain.take": ["son", "I'm only borrowing one wish."],
  "rome.fountain.again": ["son", "One wish is borrowing. Two is stealing."],
  "rome.hole.look": ["son", "It hums. Dad would say that's the wind. Dad says everything is the wind."],
  "rome.hole.use": ["son", "I'm not jumping in there again without a snack."],
  "rome.hole.coin": ["son", "Heads I find Dad. Tails he finds me."],
  "rome.hole.coin2": ["son", "... It didn't come back down."],

  // ---------- the sketch example scene ----------
  "sketch.stall": ["son", "Placeholder fruit. It tastes like a to-do list."],
  "sketch.gate": ["son", "This gate isn't drawn yet. It's still very impressive."],
  "sketch.cart": ["son", "A cart, according to the label."],
  "sketch.cart.use": ["son", "I'd push it, but it's mostly a rectangle."],

  // ---------- carried things ----------
  "item.map.look": ["dad", "A road map. It folds eleven ways and none of them is the way it came."],
  "item.reed.look": ["dad", "A reed. The pen of the future, about three thousand years ago."],
  "item.coin.look": ["son", "A coin with a serious man on it."],

  // ---------- hints: one per puzzle, spoken by the lead ----------
  "hint.egypt.reed": ["dad", "The scribe lost his pen. Something by the river might do for a new one."],
  "hint.egypt.map": ["dad", "I should check what's still in the wagon."],
  "hint.egypt.pen": ["dad", "I have a reed, and I know a man who needs a pen."],
  "hint.egypt.mark": ["dad", "The scribe wants something to draw on. A map is mostly drawing."],
  "hint.egypt.leave": ["dad", "The door is holding still now. Time to go through it."],
  "hint.rome.coin": ["son", "That fountain is full of other people's wishes."],
  "hint.rome.toss": ["son", "The humming door might like a coin."],

  // ---------- stock replies ----------
  "nope.dad.1": ["dad", "That's not how I'd do it. And I'd do almost anything."],
  "nope.dad.2": ["dad", "No. But I respect the idea."],
  "nope.dad.3": ["dad", "That won't work. Trust me, I've read half a manual."],
  "nope.son.1": ["son", "That doesn't work. I checked. In my head."],
  "nope.son.2": ["son", "Nope."],
  "look.dad.1": ["dad", "Nothing to write home about. Not that the mail goes there yet."],
  "look.son.1": ["son", "It's a thing. I'm looking at it."],
  "hint.dad.none": ["dad", "I've got nothing. Let's look around."],
  "hint.son.none": ["son", "No idea. I'll poke at things until something happens."],
};
