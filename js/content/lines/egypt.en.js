// Act One: Egypt, about 2560 B.C. Every line the four Egypt scenes speak, the hints for the act's beats, and what
// Dad says when he looks at a thing in his pockets.
//   "line.id": ["who", "What they say."]
//
// Speakers: dad, and the nine Egyptians (carrier, scribe, overseer, hauler1, hauler2, hauler3, guard, lampboy,
// goldsmith). Three rules hold all through, and briefs/out/check-egypt.mjs holds the lines to them:
//   - Dad shortens his words, and the Egyptians never do.
//   - Dad never raises his voice: there is not one exclamation mark in his lines.
//   - An Egyptian says only what is true of the time (docs/PUZZLES-egypt.md has the list, and what has been
//     checked). Dad may guess wrong out loud, and is put right.
//
// The lines marked "kept" are the author's own, from the first version of the act. They are the standard the rest
// was written to: leave them word for word. The two marked "changed" are his with a word or two altered, on purpose.
// (docs/PUZZLES-egypt.md says which of the first version's lines were dropped, and why.)

export const lines = {
  // ================= egypt-crash: where the wagon came down =================

  // ---------- arrival ----------
  "egypt.arrive.1": ["dad", "Okay. Nobody panic. The car has landed."],                                                              // kept
  "egypt.arrive.2": ["dad", "Buddy? ... Buddy?"],                                                                                    // kept
  "egypt.arrive.3": ["dad", "He was in the passenger seat a minute ago. Or a thousand years from now. I'm still working out the tenses."],   // kept
  "egypt.arrive.4": ["dad", "Sneaker prints. Small ones, going up that track."],
  "egypt.arrive.5": ["dad", "He's gone to see the biggest thing in sight. I'd be annoyed if I hadn't taught him that."],

  // ---------- the river, the bank, the far end of the track ----------
  "egypt.river.look": ["dad", "Either that's the Nile or a very committed car wash."],                                               // kept
  "egypt.river.look2": ["dad", "No hoses, no brushes, no kid with a towel. I'm calling it: the Nile."],
  "egypt.river.use": ["dad", "I'm not wading in. These are my good sandals. Also my only sandals. That's what makes them good."],
  "egypt.reeds.look": ["dad", "Reeds. Nature's ballpoint."],                                                                         // kept
  "egypt.reeds.take": ["dad", "One reed. I'll bring it back. That's a lie. I never bring pens back."],                               // kept
  "egypt.reeds.again": ["dad", "One is plenty. I'm not opening a stationery shop."],                                                 // kept
  "egypt.boat.look": ["dad", "A boat full of white stone, coming across. Even the rocks around here get a ferry."],
  "egypt.boat.look2": ["dad", "They're moving a quarry across a river, one boatload at a time. And I complain about groceries."],
  "egypt.palms.look": ["dad", "Palm trees. The only shade for miles, and it's standing exactly where I'm not."],
  "egypt.pyramids.look": ["dad", "They look brand new. Somebody kept the receipt."],                                                 // kept
  "egypt.pyramids.look2": ["dad", "It's farther off than it looks. Big things always are. I learned that from a shopping mall."],
  "egypt.footprints.look": ["dad", "Small prints, and not one straight line. He stopped to look at something every four feet. That's my boy."],
  "egypt.footprints.use": ["dad", "They go up the track, toward the pyramid. Then so do I."],
  "egypt.track.look": ["dad", "A track worn flat by a lot of feet, straight up to the pyramid. I didn't ask anybody. I want that noted."],
  "egypt.block.look": ["dad", "A dropped block and a broken sledge. Somebody's having a worse day than I am. It helps."],
  "egypt.block.use": ["dad", "I gave it a push. It's the size of a dishwasher, and it feels the same way about moving."],
  "egypt.donkey.look": ["dad", "A donkey with three water jars. Low mileage, runs on hay, never needs a jump."],
  "egypt.donkey.look2": ["dad", "Donkey the donkey. These are my kind of people."],
  "egypt.donkey.use": ["dad", "He let me scratch his ears. Friendliest anyone's been since Nevada."],
  "egypt.donkey.sunglasses": ["dad", "He gave me a look. I've had that look from a car salesman. I put them away."],

  // ---------- the wagon, and what is still in it ----------
  "egypt.wagon.look": ["dad", "Two hundred thousand miles and she still runs. Not right now. But in general."],                      // kept
  "egypt.wagon.try": ["dad", "I turned the key. She made the noise she makes when I bring up the transmission."],
  "egypt.hood.look": ["dad", "She's just thinking it over."],
  "egypt.hood.look2": ["dad", "Steam. That's her way of saying 'not now'. I get the same from the lawnmower."],
  "egypt.hood.use": ["dad", "I don't open the hood. Whatever's under there, we have an understanding."],
  "egypt.hood.flashlight": ["dad", "I looked under her with it. Sand. More sand. That's the full report."],
  "egypt.hood.rootbeer": ["dad", "She doesn't take root beer. I've never checked. I'm fairly sure."],
  "egypt.glovebox.look": ["dad", "The glovebox. Home of the map, the manual, and something that used to be mints."],
  "egypt.wagon.use": ["dad", "There's a road map in the glovebox. Three states, zero centuries."],                                   // kept
  "egypt.wagon.empty": ["dad", "Nothing left in there but ketchup packets. I'm saving those."],                                      // kept
  "egypt.mirror.look": ["dad", "The door mirror. It's shown me every wrong turn I ever made, only smaller."],
  "egypt.mirror.take": ["dad", "One twist and it's off. It's been one twist from off since March."],
  "egypt.car.noreason": ["dad", "I'm not taking my own car apart without a reason. I usually have at least a bad one."],
  "egypt.suitcase.look": ["dad", "The suitcase. I sat on it to get it shut. It hasn't forgiven me."],
  "egypt.suitcase.open": ["dad", "Six more loud shirts. The store had a deal. The store saw me coming."],
  "egypt.suitcase.take": ["dad", "Sunglasses. Right on top of six more shirts, every one of them louder than this."],
  "egypt.suitcase.again": ["dad", "Six shirts. I packed for a week of barbecues. I got one pyramid."],
  "egypt.trunk.look": ["dad", "The trunk. Everything I might need, packed under everything I won't."],
  "egypt.trunk.flashlight": ["dad", "A flashlight. I packed it in case of a flat. I did not pack it in case of Egypt."],
  "egypt.trunk.rest": ["dad", "A lawn chair, jumper cables and the windshield shade. All fine where they are."],
  "egypt.trunk.shade": ["dad", "The windshield shade. Ten years of keeping the sun out. Time it worked for the other side."],
  "egypt.trunk.after": ["dad", "A lawn chair and jumper cables. If this takes much longer, I'm getting the chair out."],
  "egypt.trunk.cables": ["dad", "Jumper cables. The nearest other battery is four and a half thousand years up the road."],
  "egypt.trunk.chair": ["dad", "A folding lawn chair. For when I've earned a sit-down. So, not yet."],
  "egypt.cooler.look": ["dad", "The cooler. Root beer, ice, and one sandwich I'm not ready to talk about."],
  "egypt.cooler.take": ["dad", "Root beer. Still cold. The ice held. Something on this trip had to."],
  "egypt.cooler.have": ["dad", "One at a time. It's a cooler, not a bar."],
  "egypt.cooler.more": ["dad", "One more. The rest are for the drive home. I'm an optimist."],

  // ---------- the water carrier, and Donkey ----------
  "egypt.carrier.look": ["dad", "An old man watering a donkey. He hasn't looked at the car once. That takes practice."],
  "egypt.carrier.hello": ["carrier", "You came down out of the sky in a red box. Nothing was pulling it."],
  "egypt.scribe.hello2": ["dad", "It has a hundred and forty horses. They're resting."],                                             // kept
  "egypt.carrier.hello2": ["carrier", "So is Donkey. Nobody calls him a hundred and forty."],
  "egypt.ask.boy": ["dad", "Have you seen a boy? About this tall, asks a lot of questions?"],                                        // kept
  "egypt.carrier.boy.1": ["carrier", "A small one in strange sandals. He went up the track, asking everyone where the 'wy-fy' was."],
  "egypt.carrier.boy.2": ["carrier", "I said it would be up at the Horizon. Everything is."],
  "egypt.carrier.boy.3": ["dad", "That's him. He asks that everywhere. It's how he says hello."],
  "egypt.carrier.ask.horizon": ["dad", "What's this Horizon everybody's at?"],
  "egypt.carrier.horizon.1": ["carrier", "The big white one, up the track. The king's. Its name is Horizon of Khufu."],
  "egypt.carrier.horizon.2": ["dad", "A pyramid called Horizon. Finally, one I can actually reach."],
  "egypt.carrier.ask.news": ["dad", "Anything I should know before I go up?"],
  "egypt.carrier.news.1": ["carrier", "A wall inside has begun to hum, and the haulers have put down the rope."],
  "egypt.carrier.news.2": ["carrier", "And the scribe's pen has split, so he can write nobody onto his list. It is a slow day."],
  "egypt.carrier.news.3": ["dad", "A humming wall and a paperwork problem. I've had Mondays like that."],
  "egypt.carrier.ask.donkey": ["dad", "Good-looking donkey. What's his name?"],
  "egypt.carrier.donkey.1": ["carrier", "Donkey."],
  "egypt.carrier.donkey.2": ["dad", "Good name. I had a goldfish called Fish. Same system."],
  "egypt.carrier.ask.camels": ["dad", "No camels? I was told there'd be camels."],
  "egypt.carrier.camels.1": ["carrier", "I do not know that word. Is it a kind of donkey?"],
  "egypt.carrier.camels.2": ["dad", "Taller. Worse attitude."],
  "egypt.carrier.camels.3": ["carrier", "Then I am glad we have none."],
  "egypt.carrier.ask.bye": ["dad", "Well. I've got a hill to climb and a boy to ground."],
  "egypt.carrier.bye": ["carrier", "Walk slowly. Everything up there has already gone wrong. You cannot be late."],
  "egypt.carrier.rootbeer.1": ["dad", "Something cold? On the house."],
  "egypt.carrier.rootbeer.2": ["carrier", "It hisses. I carry water. Water does not hiss at a man."],
  "egypt.carrier.map.1": ["carrier", "Where is the river on this?"],
  "egypt.carrier.map.2": ["dad", "There isn't one. It's Nevada."],
  "egypt.carrier.map.3": ["carrier", "Then it is a picture of nowhere. Keep it."],

  // ================= egypt-site: the foot of the pyramid =================

  // ---------- arrival, and the place ----------
  "egypt.site.arrive.1": ["dad", "So that's what they look like before the gift shop."],
  "egypt.site.arrive.2": ["overseer", "Why is nobody pulling? Why is nobody carrying? Why is everybody STANDING?"],
  "egypt.site.arrive.3": ["dad", "And that'll be the manager."],
  "egypt.site.pyramid.look": ["dad", "Smooth white stone, all the way up. Somebody waxed a mountain."],
  "egypt.site.pyramid.look2": ["dad", "Still wearing its scaffolding. Nearly done. I know 'nearly done'. I own a deck."],
  "egypt.site.small.look": ["dad", "Three small ones around the side. Everybody starts somewhere."],
  "egypt.site.entrance.look": ["dad", "A doorway up a flight of steps, under two slabs leaning like a tent. No handle. No welcome mat."],
  "egypt.site.entrance.look2": ["dad", "The way in. Up there a wall is humming a tune only my family knows."],
  "egypt.site.stair.look": ["dad", "Mud brick steps up to the door, and a rope for a handrail. The inspector's going to have notes."],
  "egypt.site.desk.look": ["dad", "Bread in baskets, beer in jars: the day's wages. I've had jobs that paid worse and tasted worse."],
  "egypt.site.desk.look2": ["dad", "Papyrus rolls, tallies scratched on bits of pot, one palette. It's an office. All it needs is a dead plant."],
  "egypt.site.sledge.look": ["dad", "A white block as high as my chest, on a wooden sled. No wheels. I'm looking at the invention of the bad back."],
  "egypt.site.sledge.look2": ["dad", "They've watered the sand in front of the runners. Like a ballfield. These people know something."],
  "egypt.site.sledge.use": ["dad", "I pulled. It didn't. We've agreed to see other people."],
  "egypt.site.blocks.look": ["dad", "Copper chisels, wooden mallets, a plumb line. Not one power tool, and it's squarer than my garage."],
  "egypt.site.blocks.use": ["dad", "I'm not touching another man's chisels. I've lent out a ladder. I know how that ends."],
  "egypt.site.sunspot.look": ["dad", "A patch of sand with the sun square on it. Nobody's standing there. They have more sense."],
  "egypt.site.sunspot.look2": ["dad", "Full sun, and a clear shot from here up to that doorway. If light were a golf ball, this is the tee."],
  "egypt.site.sunspot.use": ["dad", "I stood in it. Same sun as at home, with the dial turned all the way up."],
  "egypt.site.track.look": ["dad", "The track back down to the river, the car, and the only cold drinks in Egypt."],
  "egypt.site.rope.look": ["dad", "Rope as thick as my wrist, lying where they dropped it. I've left a garden hose out for less reason."],
  "egypt.site.scaffold.look": ["dad", "Poles lashed together with rope, four stories up. I get dizzy cleaning the gutters."],
  "egypt.site.yard.look": ["dad", "Blocks lined up by the road, waiting their turn. It's the pickup line at school, only heavier."],
  "egypt.site.water.look": ["dad", "Water jars, by the road from the river. The old man's delivery. He's the only one here on schedule."],
  "egypt.site.bricks.look": ["dad", "Mud bricks drying in the sun, beside their mold. Somebody here invented the ice cube tray."],

  // ---------- the scribe: a pen, a sheet, a pass ----------
  "egypt.scribe.look": ["dad", "He's been staring at a blank sheet for a while. I know writer's block when I see it."],              // kept
  "egypt.scribe.look2": ["dad", "He's writing again. Fast. That's a man catching up on a whole morning."],
  "egypt.scribe.meet.1": ["scribe", "Do not tell me your name. I cannot write it down, so it would only be a noise."],
  "egypt.scribe.meet.2": ["dad", "Pen trouble?"],
  "egypt.scribe.meet.3": ["scribe", "It split at dawn. Since then nothing has happened here. Not officially."],
  "egypt.scribe.boy.1": ["scribe", "There is no boy on my list. If he is not on the list, he did not go in."],
  "egypt.scribe.boy.2": ["dad", "He's not on a lot of lists. It has never once stopped him going in."],
  "egypt.scribe.ask.list": ["dad", "How does a man get onto that list of yours?"],
  "egypt.scribe.list.nopen": ["scribe", "I write him onto it. With a pen. You see the difficulty."],
  "egypt.scribe.list.nosheet": ["scribe", "I write him a pass. On a sheet. My last clean sheet is for the grain account."],
  "egypt.scribe.list.done": ["scribe", "You are on it. You are the only thing written today. A short day, but a tidy one."],
  "egypt.ask.bye": ["dad", "I'll let you get back to your sheet."],                                                                  // kept
  "egypt.ans.bye": ["scribe", "It is not going anywhere. Neither am I."],                                                            // kept
  "egypt.give.reed": ["dad", "Here. It's a pen. Some assembly required."],                                                           // kept
  "egypt.got.reed": ["scribe", "A good reed. You have the eye of a scribe and the clothes of a market stall."],                      // kept
  "egypt.scribe.rush": ["scribe", "A rush is the proper thing for a pen. But a man without one cannot be particular."],
  "egypt.scribe.supplier": ["scribe", "You have delivered one reed. That makes you a supplier. Suppliers go on the list."],
  "egypt.scribe.needsheet": ["scribe", "But the guard wants a pass, and my last clean sheet is for the grain account."],
  "egypt.give.map": ["dad", "Draw on this. It's a map. It's already wrong, you can't make it worse."],                               // kept
  "egypt.got.map.nopen": ["scribe", "A fine sheet. I have nothing to mark it with."],                                                // kept
  "egypt.scribe.pass.1": ["scribe", "'One supplier of reeds. Foreign. Loud about the shoulders.' There. Now you exist."],
  "egypt.scribe.pass.2": ["scribe", "Show the guard my side of the sheet. He knows my hand when he sees it."],
  "egypt.pass.got": ["dad", "A hall pass. Thirty years out of school and I've finally got one."],
  "egypt.scribe.rootbeer": ["scribe", "Beer made of roots. I will not enter that. The brewers would never forgive me."],
  "egypt.scribe.shade": ["scribe", "I hold a pen. It is all I hold. Ask a man with idle arms."],
  "egypt.scribe.pass": ["scribe", "I wrote it. I do not need to read it. That is the whole point of writing."],

  // ---------- the overseer: the schedule ----------
  "egypt.overseer.look": ["dad", "A big man with a staff and a schedule. I can't see the schedule. I can hear it."],
  "egypt.overseer.meet.1": ["overseer", "You. Nobody dresses like that without a reason. You are the specialist they sent for."],
  "egypt.overseer.meet.2": ["dad", "Close. I'm the generalist nobody sent for."],
  "egypt.overseer.meet.3": ["overseer", "Good. A wall inside has begun to hum. Make it stop before the inspection. Take all the time you need, today."],
  "egypt.overseer.boy.1": ["overseer", "A boy? I have a whole gang not working. I cannot also watch a boy who is not working."],
  "egypt.overseer.ask.hum": ["dad", "Tell me about this humming wall."],
  "egypt.overseer.hum.1": ["overseer", "In the chamber at the top, since dawn. Now no man will carry so much as a basket past it."],
  "egypt.overseer.hum.2": ["overseer", "I told them a wall cannot hurt them. They said a wall cannot hum either. I had no answer."],
  "egypt.overseer.hum.3": ["dad", "They've got you there."],
  "egypt.overseer.hum.4": ["overseer", "Twenty years I have built this. On time. Until a wall began to HUM."],
  "egypt.overseer.ask.schedule": ["dad", "How's the schedule holding up?"],
  "egypt.overseer.sched.0a": ["overseer", "The haulers blame the wall. The scribe blames his pen. I blame all of them. It saves time."],
  "egypt.overseer.sched.0b": ["overseer", "So you are going in. Get onto the scribe's list. The guard turns back anyone who is not on it."],
  "egypt.overseer.sched.1": ["overseer", "You have been in, and it still hums. Ask the lamp boy. He saw something, and he tells me nothing."],
  "egypt.overseer.sched.2": ["overseer", "So the boy talked to you. A little sun in a hand. Then find a little sun. I have only the big one."],
  "egypt.overseer.sched.3": ["overseer", "You say the wall wants sunlight. The sun is out here. The wall is in there. I did not plan for them to meet."],
  "egypt.overseer.sched.3b": ["overseer", "Unless you can bend the day around three corners, we are late."],
  "egypt.overseer.sched.3c": ["dad", "We're not late. We're making good time."],
  "egypt.overseer.sched.4": ["overseer", "A stripe of daylight is going into my pyramid. It is not on the schedule. Is it helping?"],
  "egypt.overseer.sched.4b": ["dad", "Like a charm."],
  "egypt.overseer.sched.4c": ["overseer", "Then it was always on the schedule."],
  "egypt.overseer.ask.bye": ["dad", "I'll get right on it."],
  "egypt.overseer.bye": ["overseer", "Get on it faster."],
  "egypt.overseer.bark.light": ["overseer", "Well? Does it still hum? No. Do not answer. I can see it in your face."],
  "egypt.overseer.bark.guard": ["overseer", "My guard is holding a shining thing at the sun. Put it on the schedule. Under 'strange'."],
  "egypt.overseer.bark.all": ["overseer", "There is DAYLIGHT going into my pyramid. Nobody told me. Nobody tells me anything."],
  "egypt.overseer.map": ["overseer", "A plan? I have a plan. I have had the same plan for twenty years. It was going very well."],
  "egypt.overseer.shade": ["overseer", "I oversee. If I stand there holding that, who oversees me holding it?"],
  "egypt.overseer.mirror": ["overseer", "Who is that tired man? ... Take it away. I have enough to worry about."],
  "egypt.overseer.rootbeer": ["overseer", "Is it medicine? No? Then it cannot help me."],

  // ---------- the haulers: one speaks, one agrees, one eats ----------
  "egypt.haulers.look": ["dad", "Three big fellows and one idle rope. One talks, one nods, one eats. It's a road crew."],
  "egypt.haulers.meet.1": ["hauler1", "Friends of Khufu. Best gang on the Horizon. We are resting."],
  "egypt.haulers.meet.2": ["hauler2", "We are resting very well."],
  "egypt.haulers.meet.3": ["hauler3", "Mm."],
  "egypt.haulers.boy.1": ["hauler1", "The small one. He asked to ride the sledge. We said no. He rode it."],
  "egypt.haulers.boy.2": ["hauler2", "He was no weight at all."],
  "egypt.haulers.boy.3": ["dad", "He's been told about riding things. I'll tell him again. It won't help."],
  "egypt.haulers.ask.break": ["dad", "Long break?"],
  "egypt.haulers.break.1": ["hauler1", "Since the wall began to hum. We pull stone. We do not pull stone toward a noise."],
  "egypt.haulers.break.2": ["hauler2", "Never toward a noise."],
  "egypt.haulers.ask.free": ["dad", "Hang in there, fellas. One day you'll all be free."],
  "egypt.haulers.free.1": ["hauler1", "Free? We are the Friends of Khufu. We are PAID. Bread and beer, every day."],
  "egypt.haulers.free.2": ["hauler2", "Every day."],
  "egypt.haulers.free.3": ["hauler3", "Mm-hm."],
  "egypt.haulers.free.4": ["dad", "Bread and beer, every day. I take it back. Are you hiring?"],
  "egypt.haulers.ask.sand": ["dad", "Why's the sand wet in front of the sledge?"],
  "egypt.haulers.sand.1": ["hauler1", "Wet the sand in front of the runners and one man pulls like two."],
  "egypt.haulers.sand.2": ["dad", "That's good. I'm trying that on the driveway."],
  "egypt.haulers.ask.bye": ["dad", "Well. Keep up the good work."],
  "egypt.haulers.bye.1": ["hauler1", "We are not doing any."],
  "egypt.haulers.bye.2": ["hauler3", "Mm."],
  "egypt.haulers.rootbeer.1": ["hauler1", "Is there beer in it?"],
  "egypt.haulers.rootbeer.2": ["dad", "No. It's root beer."],
  "egypt.haulers.rootbeer.3": ["hauler1", "Then it is a root. We are not paid in roots."],
  "egypt.haulers.rootbeer.4": ["hauler2", "Never in roots."],
  "egypt.haulers.shade.1": ["hauler1", "We pull. Holding is another trade."],
  "egypt.haulers.shade.2": ["hauler2", "A lesser trade."],

  // ---------- the guard: the stair, and then the shade ----------
  "egypt.guard.look": ["dad", "Tall, bored, and sweating through his headband. He's guarding a staircase from a patch of no shade."],
  "egypt.guard.look2": ["dad", "He's holding my windshield shade up to the sun like he's surrendering to it. It's working."],
  "egypt.guard.stop": ["guard", "Nobody goes up who is not on the scribe's list."],
  "egypt.guard.stop.2": ["dad", "I'm more of a walk-in."],
  "egypt.guard.stop.3": ["guard", "Then walk to the scribe. Under the awning."],
  "egypt.pass.show": ["dad", "One hall pass. Signed, sealed, slightly folded."],
  "egypt.guard.pass.1": ["guard", "The scribe's hand. I know it. It looks like geese in a quarrel."],
  "egypt.guard.pass.2": ["guard", "You are on the list. Go up. If it hums at you, do not bring it down here."],
  "egypt.guard.after": ["guard", "You are on the list. The stair is behind me. I am hot. That is all my news."],
  "egypt.shade.try.1": ["dad", "There. Sunlight, straight up into the doorway."],
  "egypt.shade.try.2": ["dad", "And it stops when I let go. I can't stand out here and be in there. I need a volunteer."],
  "egypt.shade.ask": ["dad", "Could you stand in the sun and hold this up? That's the whole job."],
  "egypt.guard.nohold": ["guard", "I guard. I do not hold."],
  "egypt.guard.cold": ["guard", "I would hold it for something cold. There is nothing cold. So I guard."],
  "egypt.rootbeer.give": ["dad", "Try this. It's cold. Around here that makes it treasure."],
  "egypt.guard.rootbeer": ["guard", "It bites the tongue. Like a small friendly snake."],
  "egypt.guard.owe": ["guard", "I owe you one holding. Of anything. Not heavy."],
  "egypt.guard.again": ["guard", "One snake is a friend. Two is a nest."],
  "egypt.shade.favor": ["dad", "About that holding you owe me."],
  "egypt.guard.take": ["guard", "The shining thing. In the sun. For how long?"],
  "egypt.shade.notlong": ["dad", "Not long."],
  "egypt.guard.notlong": ["guard", "The overseer says 'not long'. He has said it for twenty years."],
  "egypt.shade.lit": ["dad", "There it goes. Up the stairs and in through the door, and nobody asked it for a pass."],
  "egypt.beam.all": ["dad", "And if my mirrors are where I left them, that's going all the way in."],
  "egypt.guard.arms.1": ["guard", "My arms have gone to sleep. They are the only part of me that has."],
  "egypt.guard.arms.2": ["guard", "How long is 'not long'? In your country. In days."],
  "egypt.guard.arms.3": ["guard", "When this is over I want another of the snake water. A big one."],
  "egypt.guard.full": ["guard", "Later. My hands are full of your sun."],
  "egypt.guard.sunglasses": ["guard", "It is darker. It is not cooler. I have been cheated."],
  "egypt.guard.map": ["guard", "That is not the scribe's hand. That is a great many roads to nowhere I know."],

  // ================= egypt-gallery: inside the pyramid =================

  // ---------- arrival, and the place ----------
  "egypt.gallery.arrive.1": ["dad", "Would you look at that."],
  "egypt.gallery.arrive.2": ["dad", "A hallway four stories high, uphill, by lamplight. And me in sandals."],
  "egypt.gallery.walls.look": ["dad", "Every row of stone steps in a little closer than the one below. I get nervous hanging a shelf."],
  "egypt.gallery.walls.look2": ["dad", "It's like the hull of a ship somebody parked upside down. On purpose. Out of rock."],
  "egypt.gallery.out.look": ["dad", "Daylight, at the end of a very low passage. Watch your head. I didn't."],
  "egypt.gallery.low.look": ["dad", "A low passage, straight in under the ramp. No lamps, no hum, no small footprints."],
  "egypt.gallery.low.use": ["dad", "I put my head in and said 'Buddy?' It said 'Buddy' back, twice. Nobody home."],
  "egypt.gallery.low.flashlight": ["dad", "I shone it down there. It goes a long way into nothing. The batteries didn't enjoy it."],
  "egypt.gallery.top.look": ["dad", "A small doorway at the very top. The lamps give up before it does."],
  "egypt.gallery.top.look2": ["dad", "The way to the burial chamber, the humming wall, and the one man who can't hear it."],
  "egypt.gallery.slot.look": ["dad", "A slot cut in the stone bench. One every few feet, all the way up. The builder had a thing about slots."],
  "egypt.gallery.slot.beam": ["dad", "The sunbeam comes in and lands right here, on plain stone. Stone's a poor mirror. I checked."],
  "egypt.gallery.slot.set": ["dad", "My door mirror, wedged in a pyramid. It's never had a view like this."],
  "egypt.gallery.step.look": ["dad", "A tall step at the top of the ramp, flat as a table. A good place to stand something."],
  "egypt.gallery.step.set": ["dad", "The goldsmith's mirror, on the top step. Doing the one job he couldn't stand."],
  "egypt.gallery.marks.look": ["dad", "Red paint on the block. A straight line and some squiggles. The builders left themselves a note."],
  "egypt.gallery.marks.look2": ["dad", "I'd say it means 'this way up'. I'd be guessing. I guess with great confidence."],
  "egypt.gallery.jars.look": ["dad", "Oil jars and spare lamp dishes. The supply closet. Every big job has one, and one kid who runs it."],
  "egypt.gallery.jars.use": ["dad", "I'm not borrowing a lamp. The boy counts them. I can tell by the way he's watching me."],
  "egypt.gallery.ladder.look": ["dad", "A ladder. Good. One thing in this building I already know how to fall off."],
  "egypt.gallery.rope.look": ["dad", "A coil of rope. Around here it's the answer to everything. Like duct tape, with splinters."],
  "egypt.gallery.runner.look": ["dad", "A sled runner, worn flat. Whatever it hauled up here, it wasn't coming back down."],
  "egypt.gallery.chest.look": ["dad", "A gold-banded chest, set down halfway up. Somebody heard the hum and remembered an appointment."],
  "egypt.gallery.dinner.look": ["dad", "Bread and beer, left on the bench. A whole day's pay. That's how I know the hum is serious."],

  // ---------- the lamp boy: the only one who saw ----------
  "egypt.lampboy.look": ["dad", "A boy with a jar of oil, sitting as far from the top as the gallery allows."],
  "egypt.lampboy.meet.1": ["lampboy", "You wear strange sandals. So did the small one."],
  "egypt.lampboy.meet.2": ["dad", "He gets his feet from me."],
  "egypt.lampboy.saw.1": ["lampboy", "I saw him. I am the only one who saw."],
  "egypt.lampboy.saw.ask": ["dad", "Saw what?"],
  "egypt.lampboy.saw.2": ["lampboy", "A small one came, with a little sun in his hand."],
  "egypt.lampboy.saw.3": ["lampboy", "He pointed it at the wall and the wall opened like an eye and it took him."],
  "egypt.lampboy.saw.4": ["dad", "A little sun in his hand. That's the flashlight off his key ring."],
  "egypt.lampboy.saw.5a": ["dad", "So it opens for a light. I've got a light. A bigger one. It's in the trunk on the car."],
  "egypt.lampboy.saw.5b": ["dad", "So it opens for a light. I've got a light. A bigger one. It's right here in my pocket."],
  "egypt.lampboy.saw.5c": ["dad", "A light. I found that out the hard way. And the expensive way: those were good batteries."],
  "egypt.ask.door": ["dad", "What is the humming door?"],                                                                            // kept
  "egypt.lampboy.door.1": ["lampboy", "It is not a door. I know every door in the Horizon. I light them."],
  "egypt.lampboy.door.2": ["lampboy", "This opened where the masons put nothing."],
  "egypt.lampboy.door.3": ["dad", "That's the kind my family finds."],
  "egypt.lampboy.ask.lamps": ["dad", "You look after all these lamps yourself?"],
  "egypt.lampboy.lamps.1": ["lampboy", "Every lamp from here to the top. I fill them before they go hungry."],
  "egypt.lampboy.lamps.2": ["lampboy", "Not today. Today the top ones can go hungry. I am not going up there."],
  "egypt.lampboy.lamps.3": ["dad", "Fair. I wouldn't either. I'm going to. But I wouldn't."],
  "egypt.lampboy.ask.bye": ["dad", "Thanks. Keep the lights on."],
  "egypt.lampboy.bye": ["lampboy", "That is all I do."],
  "egypt.lampboy.sun": ["lampboy", "You brought the sun indoors. It needs no oil. I do not trust it."],
  "egypt.lampboy.flashlight": ["lampboy", "No. Keep your sun in your own hand. I saw what the small one's did."],
  "egypt.lampboy.dead.1": ["dad", "Here. A little sun of your own. It's out of sun."],
  "egypt.lampboy.dead.2": ["lampboy", "It is a lamp. Lamps I understand. I will fill it."],
  "egypt.lampboy.dead.3": ["dad", "Don't. ... No, you know what? Go ahead. See what happens."],
  "egypt.lampboy.rootbeer": ["lampboy", "It is sweet and it bites. Do not tell the overseer. He would want to count it."],
  "egypt.lampboy.sunglasses": ["lampboy", "They put out every lamp at once. I work all day to do the opposite."],

  // ---------- the two mirrors, and the sunbeam as it grows ----------
  "egypt.foot.set": ["dad", "Wedged. That's not coming out. Nothing I wedge ever does."],
  "egypt.mirror.nothing": ["dad", "A mirror with nothing to reflect. I've worked with people like that."],
  "egypt.foot.lit": ["dad", "And there it goes, straight up the ramp. It stops dead at the top step. One more corner."],
  "egypt.foot.wrong": ["dad", "It won't wedge. It wants a flat place to stand, like the rest of us."],
  "egypt.top.early": ["dad", "A mirror at the top of a dark ramp. I'd only be decorating."],
  "egypt.top.set": ["dad", "There. Tilted at the little door. He kept it polished, I'll give him that."],
  "egypt.top.dark": ["dad", "It's reflecting the dark beautifully. The daylight hasn't made it this far up."],
  "egypt.top.lit": ["dad", "And in it goes. I'd better go and see what it's found."],
  "egypt.top.wrong": ["dad", "It won't stand up on its own. It was built to hang off a door."],
  "egypt.gallery.shade": ["dad", "No sun in here to bounce. That's the whole problem."],
  "egypt.beam.in": ["dad", "There's my sunbeam. In through the passage, flat onto the bench, and stuck there."],
  "egypt.beam.up": ["dad", "Look at that. In through the passage, off my mirror and all the way up the ramp."],
  "egypt.relay.done": ["dad", "In through the passage, up the ramp, off the copper and in at the top. That's the whole relay."],

  // ================= egypt-chamber: the burial chamber =================

  // ---------- arrival, and the place ----------
  "egypt.chamber.arrive.1": ["dad", "Gold. That is a great deal of gold."],
  "egypt.chamber.arrive.2": ["dad", "And a hum. Low, like a refrigerator in the next room. There is no next room."],
  "egypt.chamber.walls.look": ["dad", "Bare red stone. Not one picture, not one word. I was promised walls you could read."],
  "egypt.chamber.walls.look2": ["dad", "No curse over the door, either. I looked. I'm a little let down."],
  "egypt.chamber.door.look": ["dad", "The little door back to the gallery. We've met. I led with my forehead."],
  "egypt.chamber.treasure.look": ["dad", "A gold bed, gold chairs, a chair for being carried around in. I respect a man who overpacks."],
  "egypt.chamber.treasure.look2": ["dad", "The bed has lion's feet. Mine has a phone book under one corner. Same idea."],
  "egypt.chamber.treasure.use": ["dad", "I'm not touching it. I can't get a hotel towel past my conscience."],
  "egypt.chamber.sarc.look": ["dad", "A stone box the size of a bathtub. No lid on, nobody in. Good."],
  "egypt.chamber.sarc.look2": ["dad", "Plain as a workbench. For a man with a gold bed, he's picked a very firm mattress."],
  "egypt.chamber.sarc.use": ["dad", "I'm not getting in. That's a one-way bath."],
  "egypt.chamber.lid.look": ["dad", "The lid, still roped, leaning on the wall. Nobody's in a hurry to need it. Least of all the king."],
  "egypt.chamber.bench.look": ["dad", "Small hammers, a blowpipe, a dish of gold leaf. All you need to make a chair too good to sit on."],
  "egypt.chamber.brazier.look": ["dad", "A little charcoal brazier, glowing away. First grill I've seen all day, and not a thing on it."],
  "egypt.chamber.mirror.look": ["dad", "A copper hand mirror, propped against a jar. Bright enough to shave in. I checked. I need a shave."],
  "egypt.chamber.mirror.use": ["dad", "Mind if I borrow that mirror?"],
  "egypt.goldsmith.mirror.no": ["goldsmith", "MY SORROW? Yes. That mirror. I check the gold in it, and it checks my face. Leave it be."],

  // ---------- the goldsmith: he mishears everything ----------
  "egypt.goldsmith.look": ["dad", "An old man gilding a small box by lamplight, squinting like the box is shining a flashlight at him."],
  "egypt.goldsmith.look2": ["dad", "He's wearing my sunglasses and humming. He's the only thing in here that should be."],
  "egypt.goldsmith.meet.1": ["dad", "Hello there."],
  "egypt.goldsmith.meet.2": ["goldsmith", "A CHAIR? Yes, it is a chair. You have good eyes. I had those once."],
  "egypt.goldsmith.meet.3": ["dad", "This is going to be a long conversation."],
  "egypt.goldsmith.boy.1": ["goldsmith", "A TOY? I do not make toys. I make furniture for the king."],
  "egypt.goldsmith.boy.2": ["dad", "A BOY."],
  "egypt.goldsmith.boy.3": ["goldsmith", "Oh. Him. He stood where you are standing. Then he was not standing there. I thought he had gone home."],
  "egypt.goldsmith.ask.hum": ["dad", "Doesn't the humming bother you?"],
  "egypt.goldsmith.hum.1": ["goldsmith", "WHAT HUM?"],
  "egypt.goldsmith.hum.2": ["goldsmith", "Fifty years with a hammer. I hear the hammer. I hear nothing else. It is very restful."],
  "egypt.goldsmith.ask.eyes": ["dad", "Are your eyes all right?"],
  "egypt.goldsmith.eyes.1": ["goldsmith", "MY PRICE? I have no price. I have sore eyes. Fifty years of gold, all of it shining at me."],
  "egypt.goldsmith.eyes.2": ["goldsmith", "I am tired of shining things. That mirror most of all. It shines AND it shows me my face."],
  "egypt.goldsmith.eyes.3": ["dad", "Tired eyes and too much glare. I packed a thing for that."],
  "egypt.goldsmith.eyes.after": ["goldsmith", "MY NIGHT? Yes. I wear the night on my nose now. Nothing shines at me in there."],
  "egypt.goldsmith.ask.king": ["dad", "All this for one pharaoh?"],
  "egypt.goldsmith.king.1": ["goldsmith", "ONE ARROW? No arrows. It is furniture. All of it for the king."],
  "egypt.goldsmith.king.2": ["dad", "The king. Right. One of those."],
  "egypt.goldsmith.ask.bye": ["dad", "Good talking to you."],
  "egypt.goldsmith.bye": ["goldsmith", "WALKING? You were not walking. You stood there the whole time. I saw you."],
  "egypt.goldsmith.trade.1": ["dad", "Try these. They turn the brightness down."],
  "egypt.goldsmith.trade.2": ["goldsmith", "FROWN? I am not frowning. I am squinting. It is a different thing."],
  "egypt.goldsmith.trade.3": ["goldsmith", "Oh. ... Oh, that is kind. The whole world has gone the color of good beer."],
  "egypt.goldsmith.trade.4": ["goldsmith", "I never want to see a shining thing again. That mirror least of all. Take it. Take it away."],
  "egypt.goldsmith.trade.5": ["dad", "A copper mirror for a pair of drugstore sunglasses. I've finally come out ahead on a trade."],
  "egypt.goldsmith.trade.early": ["dad", "I don't know what I'll do with a mirror. That has never stopped me taking anything."],
  "egypt.goldsmith.rootbeer": ["goldsmith", "GOOD BEER? ... No. Somebody has played a trick on beer."],
  "egypt.goldsmith.flashlight": ["goldsmith", "Put it OUT. I have enough bright in here."],
  "egypt.goldsmith.pass": ["goldsmith", "A LIST? I am on the list. I have been on the list for fifty years."],
  "egypt.goldsmith.carmirror": ["goldsmith", "ANOTHER mirror? Is this a joke? Who sent you?"],
  "egypt.goldsmith.copper": ["goldsmith", "No. NO. It is yours now. Let it shine at you."],

  // ---------- the wall that hums: the flashlight, and the rule ----------
  "egypt.hum.look": ["dad", "Bare wall, empty air, a clean ring swept on the floor. And a hum. Probably the wind."],
  "egypt.hum.look2": ["dad", "It's shut, you can't see it, and it only opens for light. My son found the one door in history with a dimmer."],
  "egypt.hum.use": ["dad", "I knocked on the air. It's like knocking on a door from the wrong side. Nobody came."],
  "egypt.hum.use2": ["dad", "It wants light. A lot more than I carry in my pockets."],
  "egypt.hum.mirror": ["dad", "I showed the wall its own reflection. Nothing. It's not vain."],
  "egypt.hum.shade": ["dad", "Shading a door from the light is the exact opposite of the plan."],
  "egypt.flash.1": ["dad", "A little sun, the boy said. Let's try a medium one."],
  "egypt.flash.1b": ["dad", "Dark room, strange wall. This is what the flashlight's for."],
  "egypt.hole.look": ["dad", "A hole in the air the size of a dinner plate. I am not the size of a dinner plate."],            // kept
  "egypt.hole.small": ["dad", "It shrinks every time I get close. I have the same effect on waiters."],                             // kept
  "egypt.flash.dies": ["dad", "And there go the batteries. They were supposed to last till the motel."],
  "egypt.flash.son": ["dad", "That's what he did. A key-ring light, a hole in the air, and a boy who can't leave things alone."],
  "egypt.flash.rule.1": ["dad", "So that's the trick. Light opens it. A little light, a little door."],
  "egypt.flash.rule.2": ["dad", "More light, more door. And there's a whole sun going to waste outside."],
  "egypt.flash.dead": ["dad", "Dead. I've shaken it. Shaking is all I know about batteries."],
  "egypt.goldsmith.flash": ["goldsmith", "Did you say something? Never mind. I would not have heard it."],

  // ---------- the gate ----------
  "egypt.gate.1": ["dad", "Here it comes. Around three corners and in through the door, like it pays rent."],
  "egypt.hole.big": ["dad", "Now that's a door."],                                                                                   // kept
  "egypt.gate.gold": ["goldsmith", "Somebody has let the day in. Let it look. I am wearing the night."],
  "egypt.hole.go": ["dad", "Hold on, buddy. Dad's taking the next shortcut."],                                                       // kept
  "egypt.hole.wait": ["dad", "Not until I know where it comes out. I've made that mistake once today."],                             // kept

  // ================= carried things =================
  "item.map.look": ["dad", "A road map. It folds eleven ways and none of them is the way it came."],                                 // kept
  "item.reed.look": ["dad", "A reed. The pen of the future, about four and a half thousand years ago."],                             // changed: was "three thousand"
  "item.pass.look": ["dad", "My work pass, on the back of Nevada. Supplier of reeds. Loud about the shoulders."],
  "item.flashlight.look": ["dad", "A flashlight. The batteries are from two vacations ago. So is my faith in them."],
  "item.rootbeer.look": ["dad", "Root beer. The only cold thing in the country, and I'm carrying it in my shorts."],
  "item.shade.look": ["dad", "The windshield shade. Shiny side out. Unlike the map, it folds the way it came."],
  "item.carmirror.look": ["dad", "The door mirror. Things in it are closer than they appear. I wish that worked on home."],
  "item.sunglasses.look": ["dad", "Sunglasses. They make everything look like late afternoon. I do my best work in late afternoon."],
  "item.coppermirror.look": ["dad", "A hand mirror of polished copper. I look like a penny with a moustache."],

  // ================= hints: one for each puzzle, in Dad's own voice =================
  "hint.egypt.map": ["dad", "I should check what's still in the wagon."],                                                            // kept
  "hint.egypt.reed": ["dad", "The scribe's pen has split. Something by the river might do for a new one."],                          // changed: was "The scribe lost his pen."
  "hint.egypt.pen": ["dad", "I have a reed, and I know a man who needs a pen."],                                                     // kept
  "hint.egypt.mark": ["dad", "The scribe wants something to draw on. A map is mostly drawing."],                                     // kept (now the hint of "egypt.pass")
  "hint.egypt.inside": ["dad", "I'm on the list, and I've got the pass to prove it. The guard at the stairs ought to see it."],
  "hint.egypt.witness": ["dad", "Somebody in that pyramid saw what happened. The boy with the lamps has the look of a witness."],
  "hint.egypt.flash": ["dad", "A little sun in his hand: a flashlight. I packed one of those. And the wall that hums is at the top of the gallery."],
  "hint.egypt.shade": ["dad", "The windshield shade could throw the sun into that doorway, if somebody held it. The guard looks thirsty."],
  "hint.egypt.carmirror": ["dad", "The sunbeam has to turn at the foot of the gallery. The car has a mirror it isn't using."],
  "hint.egypt.trade": ["dad", "The goldsmith has a mirror, and eyes that are tired of shining things. I packed sunglasses."],
  "hint.egypt.topmirror": ["dad", "The copper mirror belongs on the step at the top of the gallery, to turn the light into the chamber."],
  "hint.egypt.leave": ["dad", "The door is holding still now. Time to go through it."],                                              // kept
};
