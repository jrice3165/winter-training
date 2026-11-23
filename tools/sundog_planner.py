"""Sundog Winter Training (test): 5 tracks x 5 drills, Sundog materials only.

Run:  python3 -c "import sundog_planner as p; p.write('../sundog/data/training-curriculum.json')"
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sundog_data
from planner_data import clean, GEAR as _GEAR

S = {s["id"]: s for s in sundog_data.SKILLS}

def label(code):
    if code == "F05A": return "Sundog Foundation wk 5 handout"
    if code == "F13V": return "Sundog Foundation wk 13 video"
    if code == "F14V": return "Sundog Foundation wk 14 video"
    if code.startswith("PK"): return "Sundog Puppy K wk " + code[2:]
    if code == "F08": return "Sundog Foundation wk 8–9"
    return "Sundog Foundation wk " + code[1:].lstrip("0")

TRACKS = [
  dict(id="focus", name="Focus & Connection",
       blurb="A dog who checks in with you, loves your hands, and understands your marker words.",
       drills=["name_game", "yes_marker", "charge_clicker", "hand_target", "cookie_fingers"],
       alternates=["push_away_and_run", "find_scatter", "informal_recall_cue"]),
  dict(id="calm", name="Self-Control & Calm",
       blurb="It's Your Choice games: good things come from waiting and choosing well.",
       drills=["its_your_choice", "take_it", "leave_it", "crate_games", "mat_work"],
       alternates=["sit_and_stays", "play_and_settle"]),
  dict(id="body", name="Body Awareness",
       blurb="New surfaces, shaping and back-end awareness: confidence and coordination for indoor days.",
       drills=["novel_surfaces", "shaping", "clicker_challenge", "perch_work", "two_on_two_off"],
       alternates=["hand_target"]),
  dict(id="life", name="Life Skills & Recall",
       blurb="Being caught, being handled, settling, letting go, and coming when called (hallway edition).",
       drills=["collar_grab", "play_and_settle", "tug_and_out", "loose_leash_walking", "restrained_recall"],
       alternates=["collar_body_hold", "meet_and_greet", "recall_here_come", "build_toy_drive"]),
  dict(id="agility", name="Agility Foundations",
       blurb="Flatwork you can do in a living room: position, sends, crosses and turns.",
       drills=["circle_work", "send_to_target_plate", "blind_cross_flat", "lap_turn", "wrap"],
       alternates=["connection_and_guiding_hand"]),
]

GEAR = dict(_GEAR)
GEAR.update({
  "yes_marker": ["Small treats", "Nothing else: just your voice"],
  "push_away_and_run": ["Clear hallway or open room", "Tug toy for when they catch you"],
  "informal_recall_cue": ["Treats in a pocket", "A fun, high-pitched voice"],
  "sit_and_stays": ["Small treats in an open hand", "Non-slip rug"],
  "collar_body_hold": ["A calm moment (after a walk or meal)", "A helper with treats (optional)"],
  "meet_and_greet": ["A visitor who'll ignore the pup at first", "Kitchen chair", "Leash"],
  "recall_here_come": ["Your best rewards, saved for this", "Hallway or basement"],
  "blind_cross_flat": ["A helper to hold the dog", "Treat or toy in each hand", "Hallway"],
  "clicker_challenge": ["Shallow cardboard box", "Two small books", "Clicker"],
  "novel_surfaces": ["Flattened cardboard box", "Exercise platform or yoga mat", "Contact board if you have one"],
  "perch_work": ["Perch or a sturdy upside-down tub", "Soft treats"],
  "build_toy_drive": ["Throwable toy that doesn't roll (tug rope, ball in a sock)", "3 m light line tied to it", "A drawer to keep it in"],
  "connection_and_guiding_hand": ["Treats in your non-guiding hand", "Target plate or bowl on the floor", "Toy"],
  "two_on_two_off": ["Sturdy board or the bottom stair as the 'contact'", "Target plate or bowl"],
})

# Humans-only bonuses. Ideas and links come from the Sundog notes where possible;
# the rest are simple at-home activities (balance, baking, prep).
BONUS = {
 "focus": [
   dict(kind="Watch", title="See shaping in action", text="The Week 7 video: a 12-week puppy learns to back onto an object. Notice exactly when the trainer clicks and how the criteria change.", link="https://youtu.be/CpA25qUBxiA"),
   dict(kind="Practise", title="Play the Shaping Game", text="From Week 7: one person leaves the room, the others pick a behaviour. Click only, with no words or pointing. You'll feel how much timing matters."),
   dict(kind="Make", title="Prep a week of treats", text="Week 2 says to have treats ready before every session. Cut a variety into pea-sized pieces and bag them 5–8 per exercise."),
   dict(kind="Move", title="Work on your balance", text="Stand on one foot for 30 seconds while you brush your teeth, then switch. Next, walk heel-to-toe down the hallway."),
   dict(kind="Read", title="Write down your verbals", text="From Week 3: name = head check, 'Here' = come right to me, 'Good' = keep going, 'Yes' = done, reward coming. Add 'Ready' and 'Get It'. Post them on the fridge."),
 ],
 "calm": [
   dict(kind="Bake", title="Bake pumpkin oat treats", text="Mix 1 cup oat flour, ½ cup plain pumpkin purée and 2 tbsp xylitol-free peanut butter. Roll, cut small, bake at 350°F for about 20 minutes. Cool; keep refrigerated."),
   dict(kind="Watch", title="Crate value video", text="The Week 3 video on starting dogs to value their crate. Watch how fast the reward follows going in.", link="https://youtu.be/FQ7evQmSWYk"),
   dict(kind="Move", title="Calm breathing break", text="Five slow breaths: in for 4, out for 6. Dogs read body language first, so a calm handler makes calm games easier."),
   dict(kind="Make", title="Fill and freeze Kongs", text="Puppy K Week 4 uses a Kong to settle on the mat. Stuff three with soaked kibble and freeze them for the week."),
   dict(kind="Practise", title="Rehearse It's Your Choice timing", text="Without the dog: hold treats in an open palm and practise snapping it closed and open fast. You have about 1 second to make the consequence clear."),
 ],
 "body": [
   dict(kind="Move", title="Work on your balance", text="Stand on a folded towel on one leg for 20 seconds each side. Feel what your dog feels on a wobbly surface."),
   dict(kind="Practise", title="Shaping Game, round two", text="Week 7's game again, harder: shape a family member to stand with both feet in a laundry basket. Notice how a late click sends them the wrong way."),
   dict(kind="Make", title="Set up a clicker challenge kit", text="From Weeks 11–12: find a shallow box and two small books, and keep them in a bag with a clicker so challenges are ready to go."),
   dict(kind="Make", title="Load a feeding spatula", text="Week 2's tip: a spatula with peanut butter, cheese spread or cream cheese lets you reward without bending over. Great for small dogs and perch work."),
   dict(kind="Read", title="Plan your contact cue", text="From Week 18: choose one release word for 2on2off ('OK', 'Break' or 'Alright') and use it from day one."),
 ],
 "life": [
   dict(kind="Practise", title="Rehearse the vet hold", text="Puppy K Week 2's collar & body hold: practise the arm positions on a stuffed animal until they're smooth."),
   dict(kind="Make", title="Make a second tug toy", text="'Out' trades need two equally loved toys (Puppy K Week 2). Braid two old tea towels into a tug with a handle loop."),
   dict(kind="Move", title="Brisk hallway laps", text="Puppy K Week 1: loose-leash walking works best at a 'late for something' pace. Walk 3 minutes of hallway laps with crisp 180° turns."),
   dict(kind="Read", title="Read the toy drive handout", text="Re-read the Week 5 handout (Susan Garrett's 'How to Create a Motivating Toy'), then pick the toy and the drawer you'll use."),
   dict(kind="Read", title="Rank your rewards", text="Week 5: 'Here' is an emergency command used only with great rewards. List your dog's top 5 and save the top two for recalls."),
 ],
 "agility": [
   dict(kind="Practise", title="Footwork without the dog", text="Walk the Week 13 lap-turn pattern around a chair: back up, dog-side leg and arm back, wait, then step forward. Do both sides until it feels like a dance."),
   dict(kind="Watch", title="Circle work video", text="The Week 3 circle work clip. Watch the dog's position at the handler's side on the curve.", link="https://youtu.be/6OHVdhE9DqY"),
   dict(kind="Read", title="Why flatwork matters", text="Weeks 4 and 6: your dog spends more time between obstacles than on them, so that's where handling happens. Re-read those notes before class."),
   dict(kind="Move", title="Quick-feet drill", text="Three steps forward, pivot, three steps back, 5 times each way. Agility handlers need nimble feet too."),
   dict(kind="Make", title="Make target plates", text="Week 6's target plate: cut three plastic lids or paper plates and add a strip of coloured tape so your dog can spot them on any floor."),
 ],
}

def drill(i):
    s = S[i]
    prog = s.get("progressions", [])
    tips = [t for t in s.get("tips", []) if "http" not in t]
    return dict(id=i, name=s["name"], purpose=s["purpose"], level=s["level"],
                cues=s.get("cues", []), steps=[clean(x) for x in s.get("how_to", [])[:7]],
                next=clean(prog[0]["text"]) if prog else None,
                tip=clean(tips[0]) if tips else None, gear=GEAR[i],
                source=", ".join(sorted({label(c) for c in s["sources"]})))

OUT = dict(
    tracks=[dict(id=t["id"], name=t["name"], blurb=t["blurb"],
                 days=[dict(drill=drill(d), bonus=b) for d, b in zip(t["drills"], BONUS[t["id"]])],
                 alternates=[drill(a) for a in t["alternates"]]) for t in TRACKS],
    bonusPool=[b for t in TRACKS for b in BONUS[t["id"]]])
for i, b in enumerate(OUT["bonusPool"]): b["id"] = f"b{i+1}"
for t in OUT["tracks"]: assert len(t["days"]) == 5

def write(path):
    for tr in OUT["tracks"]:
        for d in [x["drill"] for x in tr["days"]] + tr["alternates"]:
            if d["id"] == "lap_turn": d["img"] = "assets/lap-turn-week13.gif"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(dict(version=1, app="Sundog Winter Training (test)", dogProfile=dict(name="Sunny"), **OUT),
              open(path, "w"), indent=2, ensure_ascii=False)
