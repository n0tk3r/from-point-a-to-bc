// Act Three: home, that evening. A beat with three leads carries one hint from each of them.

const family = (id) => ({ mom: `hint.${id}.mom`, bigsis: `hint.${id}.bigsis`, lilsis: `hint.${id}.lilsis` });

export const act = {
  id: 3, title: "Act Three: Five Places Set", era: "home", gate: "home.left",
  summary: "The present, that evening. Dinner is cold and two chairs are empty. Mom and the girls set out to learn where Dad's phone was last seen: Little Sister gets the router going from inside the closet under the stairs, Big Sister works out the password from a date she happens to know, and Mom answers the one question only she can.",
  beats: [
    { id: "home.arrive", kind: "cutscene", title: "Voicemail, for the ninth time", lead: "family", scene: "home-living-room", needs: ["rome.tossed"], sets: "home.arrived" },
    { id: "home.router", kind: "puzzle", chain: "A", title: "Plug the router back in, from inside the closet", lead: "lilsis", scene: "home-living-room", needs: ["home.arrived"], sets: "home.online", hint: family("home.router") },
    { id: "home.note", kind: "puzzle", chain: "B", title: "Work out the password from Dad's note", lead: "bigsis", scene: "home-living-room", needs: ["home.arrived"], sets: "home.knowsYear", hint: family("home.note") },
    { id: "home.login", kind: "puzzle", chain: "C", title: "Sign in, and answer the question about the wedding", lead: "mom", scene: "home-living-room", needs: ["home.online", "home.knowsYear"], sets: "home.foundPing", hint: family("home.login") },
    { id: "home.leave", kind: "gate", title: "Out of the front door, to Nevada", lead: "family", scene: "home-living-room", needs: ["home.foundPing"], sets: "home.left", hint: family("home.leave") },
  ],
};
