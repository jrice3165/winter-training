"""Sundog-only view of the skill library.

Takes tools/data.py (which mixes Sundog class notes, personal notes and
external links) and keeps only what came from Sundog Agility materials:
Foundation class notes (F02-F18), Puppy Kindergarten notes (PK1-PK4),
the Week 13 diagram, the Week 13/14 videos, and the Week 5 toy-drive
handout (a Susan Garrett article distributed in class).

Anything sourced only from personal notes ("NOTES") or from outside links
is removed. Skills that mixed both have their personal-notes content
stripped or rewritten from the class notes below.
"""
import copy
import data as _all

PERSONAL_ONLY = {"off", "feet", "shake", "dance", "between", "around_cone", "flip_away", "door_waits"}

OVERRIDES = {
    "cookie_fingers": dict(
        how_to=["Treat in hand, held at the dog's nose height.",
                "Shake your wrist up and down as you move; the dog follows your hand.",
                "Practise on both sides."],
        tips=["Teaches your dog to pay attention to your body language and the value of your hand. It's the beginning step for many agility handling moves.",
              "For handling, keep cookie fingers low, by your knee (Week 13)."],
        builds_toward=["lap_turn", "send_to_target_plate"]),
    "hand_target": dict(tips=["A great way to distract or refocus your puppy."]),
    "its_your_choice": dict(
        aka=["Mugging Game"],
        tips=["Timing matters: open and close your hand at the right moment by reading body language. Dogs have about 1 second to connect a consequence.",
              "Dogs respond to body language first and words second. Less is more: say nothing during this game.",
              "The crate-door game is 'another It's Your Choice game' (Week 3)."]),
    "leave_it": dict(
        programs=["foundation"],
        how_to=["Lead your dog to a food container (or a toy) and let them sniff.",
                "Say 'Leave It' to redirect them, then feed a yummy treat from you.",
                "Repeat a few times.",
                "Then play 'This and That': say 'Ready'... 'Get It' and let them have it, so they learn the difference between not allowed and allowed."],
        tips=["Real-life payoff: food dropped on a broken-glass kitchen floor. 'Leave It' buys time to put the dogs somewhere safe.",
              "In agility, a toy on the ground is often the reward after the dog does something right; 'Leave It' keeps them from self-rewarding."]),
    "take_it": dict(
        name="'Ready' / 'Get It' & 'This and That'",
        purpose="Permission words. 'Ready' means get ready, look ahead and focus; 'Get It' means go ahead and take it. Builds excitement, self-control, and stops self-rewarding.",
        programs=["foundation"], cues=["Ready", "Get It"],
        how_to=["Hold your dog's collar with one hand and a treat about 2 ft from their face in the other.",
                "Say 'Ready'. When they're focused, release with 'Get It'.",
                "'This and That': after a few 'Leave It' reps with a food container, say 'Ready'... 'Get It' and let them have it.",
                "Use the same words for toys."],
        tips=["Use the words consistently. They tell the dog to focus and give permission to go."],
        builds_toward=["send_to_target_plate"]),
    "mat_work": dict(name="Mat work ('Go to bed')", aka=["Go to Bed"], tips=["Don't cue 'down' on the mat. Lure into the down so the mat itself comes to mean 'lie down and relax'."]),
    "novel_surfaces": dict(
        name="Luring onto objects & new surfaces", aka=[],
        cues=["Good", "Yes"],
        equipment=["contact board, a piece of cardboard, or an exercise platform"],
        how_to=["Lure the dog onto and across the new surface; give lots of cookies even for trying.",
                "Lure onto other objects and slowly increase the time they stay on.",
                "Use 'Good' to say keep going, then 'Yes' and reward when the exercise is over."],
        tips=["Builds confidence; it's the first step toward perch work and contacts."],
        builds_toward=["perch_work"]),
    "perch_work": dict(
        name="Perch work & moving off pressure",
        aka=["Hind end awareness", "Rear end awareness", "Moving off pressure"],
        equipment=["perch or other sturdy object", "treats"],
        how_to=["Start once your dog happily stands on novel objects for a few seconds.",
                "Lure, or shape with the clicker, the two front feet onto the perch.",
                "Step into your dog. The pressure moves their hind end away from you while the front feet stay on.",
                "When the hind end moves, say 'Yes' (or click) and reward.",
                "Start with one step; over time build to a full circle.",
                "Practise both clockwise and anti-clockwise."],
        tips=["Builds rear-end awareness, muscle tone, and balance on both sides.",
              "Teaches the dog that it has a front end and a back end, and to move away from handler pressure."]),
    "lap_turn": dict(prerequisites=["cookie_fingers"]),
    "name_game": dict(tips=["Name = 'head check' (look at me and wait for the next instruction), not 'come here'. In agility the name is a redirect.",
                            "Have a throwaway cue too, so the name never gets 'spoiled'.",
                            "Great for waiting your turn in class."]),
    "recall_here_come": dict(how_to=["Use ONLY with great rewards.",
                                     "With multiple dogs: name first (gets that dog's head check), then 'Here'.",
                                     "Train it with restrained recalls."]),
    "build_toy_drive": dict(name="Building toy drive (Week 5 handout)",
                            tips=["From 'How to Create a Motivating Toy' by Susan Garrett, handed out in Foundation Week 5.",
                                  "Food-mad, toy-indifferent dogs: simmer the toy in liver or chicken broth, but NEVER leave the dog alone with it.",
                                  "Be sincerely having fun or it won't work. No cues for anything during the routine.",
                                  "Remove other toys while doing this; leave only chews. Works especially well with puppies."]),
}

NEW_SKILLS = [
    dict(id="clicker_challenge", name="Clicker challenge: box & two books", category="body_awareness", level=2,
         programs=["foundation"], sources=["F11", "F12"], cues=["(click)"],
         purpose="A body-awareness puzzle: clicker train your dog to stand in a box with all 4 feet, or with front feet on 2 separate objects.",
         equipment=["shallow box", "two small books", "clicker", "treats"],
         how_to=["Review a nose touch on an object first.",
                 "Put down a shallow box (or two small books). No words, no luring.",
                 "Click & feed for looking at it, stepping toward it, any foot in or on it.",
                 "Raise criteria a little at a time: one foot, two feet, then all four (or both front feet on the two books).",
                 "Change the challenge each session, and bring your items to class to show what you've been working on."],
         tips=["Builds a thinking dog that offers behaviours, works through a hard task, and gains mental stamina."],
         prerequisites=["shaping"]),
]


def _sundog_skills():
    out = []
    for s in _all.SKILLS:
        if s["id"] in PERSONAL_ONLY:
            continue
        s = copy.deepcopy(s)
        s["sources"] = [x for x in s["sources"] if x != "NOTES"]
        s["programs"] = [p for p in s["programs"] if p != "personal"] or ["foundation"]
        s["progressions"] = [p for p in s.get("progressions", []) if p["source"] != "NOTES"]
        s.pop("gaps", None)
        s.update(copy.deepcopy(OVERRIDES.get(s["id"], {})))
        out.append(s)
    out += copy.deepcopy(NEW_SKILLS)
    keep = {s["id"] for s in out}
    for s in out:
        s["prerequisites"] = [p for p in s.get("prerequisites", []) if p in keep]
        s["builds_toward"] = [p for p in s.get("builds_toward", []) if p in keep]
        s["tips"] = [t for t in s.get("tips", []) if "your notes" not in t.lower()]
    return out


SKILLS = _sundog_skills()
SOURCES = [s for s in _all.SOURCES if s[0] != "NOTES"]
CATEGORIES = [c for c in _all.CATEGORIES if c[0] != "tricks"]
CUES = []
for c, m, alts, srcs in _all.CUES:
    srcs = [x for x in srcs if x != "NOTES"]
    if srcs:
        CUES.append((c, m, [a for a in alts if a != "Take It"], srcs))
GLOSSARY = _all.GLOSSARY
SUNDOG_LINK_SOURCES = {"Shape Up Agility (YouTube, from F03)", "YouTube (from F03)", "YouTube (from F07)"}
RESOURCES = [copy.deepcopy(r) for r in _all.RESOURCES if r["publisher"] in SUNDOG_LINK_SOURCES]
# keep resource 'related' ids valid
_ids = {s["id"] for s in SKILLS}
for r in RESOURCES:
    r["related"] = [x for x in r["related"] if x in _ids]

# ---- the other two buckets -------------------------------------------------
PERSONAL_SKILLS = [s for s in _all.SKILLS if "NOTES" in s["sources"]]
EXTERNAL_RESOURCES = [r for r in _all.RESOURCES if r["publisher"] not in SUNDOG_LINK_SOURCES]
