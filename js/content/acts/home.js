// Act Three: home, that evening. A beat with three leads carries one hint from each of them:
// the one whose job it is says what to try, and the other two say whose job it is.
//
// Five chains. A opens Dad's study (the riddle on its door, the key in the piano). B is the router, in the
// closet under the stairs: too dark without Little Sister's flashlight, which is in her fort and dead, and the
// only batteries are in Big Sister's sound machine, up in the attic. C, D and E are behind the study door: the
// family computer (C, which also needs B), the answering machine (D) and the family vault (E). The gate needs
// the end of all three.

const family = (id) => ({ mom: `hint.${id}.mom`, bigsis: `hint.${id}.bigsis`, lilsis: `hint.${id}.lilsis` });

export const act = {
  id: 3, title: "Act Three: Five Places Set", era: "home", gate: "home.left",
  summary: "The present, that evening. Dinner is cold and two chairs are empty. Mom prays first, and then the three of them go through the house: a key hidden in the piano opens Dad's study, Little Sister fetches her own flashlight from her fort and finds it dead, Big Sister gives up the batteries out of her sound machine (the Retreat goes dark so that the internet may live), Little Sister takes the light into the closet under the stairs and plugs the router in, Big Sister works out a password from a date she happens to know, and Mom answers the wedding question, winds a tape with a pencil and opens the family vault with the year the Constitution was signed. They leave for Nevada knowing where the phone was last seen, with Dad's last message in their ears and a car key in hand.",
  beats: [
    { id: "home.arrive", kind: "cutscene", title: "Voicemail, for the ninth time (and a prayer)", lead: "family", scene: "home-living-room", needs: ["rome.tossed"], sets: "home.arrived" },
    { id: "home.riddle", kind: "puzzle", chain: "A", title: "Read Dad's notice on the study door: the other eighty-eight", lead: ["bigsis", "mom"], scene: "home-landing", needs: ["home.arrived"], sets: "home.keyInPiano", hint: family("home.riddle") },
    { id: "home.key", kind: "puzzle", chain: "A", title: "Get the key out of the piano, from under the keyboard", lead: "lilsis", scene: "home-living-room", needs: ["home.keyInPiano"], sets: "home.hasKey", hint: family("home.key") },
    { id: "home.study", kind: "puzzle", chain: "A", title: "Unlock Trip Headquarters", lead: "family", scene: "home-landing", needs: ["home.hasKey"], sets: "home.studyOpen", hint: family("home.study") },
    { id: "home.batteries", kind: "puzzle", chain: "B", title: "A light for the closet: her flashlight is dead, and the only batteries are in Big Sister's sound machine", lead: ["lilsis", "bigsis"], scene: "home-bigsis-room", needs: ["home.arrived"], sets: "home.flashWorks", hint: family("home.batteries") },
    { id: "home.router", kind: "puzzle", chain: "B", title: "Plug the router back in, in the dark of the closet, by flashlight", lead: "lilsis", scene: "home-living-room", needs: ["home.flashWorks"], sets: "home.online", hint: family("home.router") },
    { id: "home.note", kind: "puzzle", chain: "C", title: "Work out the password from Dad's note", lead: "bigsis", scene: "home-study", needs: ["home.studyOpen"], sets: "home.knowsYear", hint: family("home.note") },
    { id: "home.login", kind: "puzzle", chain: "C", title: "Sign in, and answer the question about the wedding", lead: "mom", scene: "home-study", needs: ["home.online", "home.knowsYear"], sets: "home.foundPing", hint: family("home.login") },
    { id: "home.tape", kind: "puzzle", chain: "D", title: "Wind the answering machine's tape back in with Dad's pencil", lead: "mom", scene: "home-study", needs: ["home.studyOpen"], sets: "home.tapeWound", hint: family("home.tape") },
    { id: "home.message", kind: "puzzle", chain: "D", title: "Press play: Dad's last message", lead: "family", scene: "home-study", needs: ["home.tapeWound"], sets: "home.heardMessage", hint: family("home.message") },
    { id: "home.vault", kind: "puzzle", chain: "E", title: "Open the family vault: the year We the People got it in writing", lead: "mom", scene: "home-study", needs: ["home.studyOpen"], sets: "home.hasCarKey", hint: family("home.vault") },
    { id: "home.leave", kind: "gate", title: "Out of the front door, to Nevada", lead: "family", scene: "home-living-room", needs: ["home.foundPing", "home.heardMessage", "home.hasCarKey"], sets: "home.left", hint: family("home.leave") },
  ],
};
