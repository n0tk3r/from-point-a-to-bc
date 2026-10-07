// The prologue: the opening movie.

export const act = {
  id: 0, title: "Prologue: The Shortcut", era: "present", gate: "seen.intro",
  summary: "Dad takes a shortcut. The sky opens, the road sign changes its mind, and the wagon drives into a hole in time. Father and son are pulled apart in the tunnel.",
  beats: [
    { id: "intro", kind: "cutscene", title: "The shortcut", lead: "both", scene: "intro", needs: [], sets: "seen.intro" },
  ],
};
