// The story as data. js/content/story.js lists the acts, and inside each act the
// beats: cutscenes, puzzles and the gate that ends the act. A beat says which facts
// it needs and which fact it sets when done. From that one list the game gets:
//   - hints (what is open to the player right now),
//   - a storyboard page (tools/storyboard.html),
//   - a check that the story can be finished, run every time the game starts.
//
// How this keeps the game guided but not linear: within an act several beats are
// open at once, so the player picks the order. The act's gate needs all of them,
// so everybody arrives at the same closing cutscene.

export function allBeats(story) {
  return story.acts.flatMap((act) => act.beats.map((beat) => ({ ...beat, act: act.id })));
}

/** Beats the player could finish now: everything they need is true, and they are not done. */
export function openBeats(story, flags) {
  return allBeats(story).filter((b) => !flags[b.sets] && (b.needs || []).every((n) => flags[n]));
}

/** The first act whose gate has not been passed. */
export function currentAct(story, flags) {
  return story.acts.find((act) => !flags[act.gate]) || story.acts[story.acts.length - 1];
}

/** Look for mistakes in the story data. Returns a list of plain sentences. */
export function checkStory({ story, scenes, cutscenes = {}, lines = {} }) {
  const problems = [];
  const beats = allBeats(story);
  const set = new Set(beats.map((b) => b.sets));
  const seen = new Set();
  for (const b of beats) {
    if (seen.has(b.id)) problems.push(`Two beats are called "${b.id}".`);
    seen.add(b.id);
    if (!b.sets) problems.push(`Beat "${b.id}" does not set a fact, so the game cannot tell when it is done.`);
    for (const n of b.needs || []) if (!set.has(n)) problems.push(`Beat "${b.id}" needs "${n}", which no beat sets.`);
    if (b.scene && !scenes[b.scene] && !cutscenes[b.scene]) problems.push(`Beat "${b.id}" happens in "${b.scene}", which does not exist yet.`);
    if (b.hint && !lines[b.hint]) problems.push(`Beat "${b.id}" has the hint "${b.hint}", which is not in the lines file.`);
  }
  for (const act of story.acts) {
    if (act.gate && !set.has(act.gate)) problems.push(`Act "${act.title}" ends on "${act.gate}", which no beat sets.`);
  }
  // Walk the story the way a player would and see what can never be reached.
  const have = new Set();
  for (let grew = true; grew; ) {
    grew = false;
    for (const b of beats) {
      if (!have.has(b.sets) && (b.needs || []).every((n) => have.has(n))) { have.add(b.sets); grew = true; }
    }
  }
  for (const b of beats) if (b.sets && !have.has(b.sets)) problems.push(`Beat "${b.id}" can never be reached.`);
  return problems;
}
