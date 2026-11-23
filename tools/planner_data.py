"""Winter Training planner: 5 tracks x 5 drills, drawn from data.SKILLS."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import data

S = {s["id"]: s for s in data.SKILLS}
WEEK = {"PK1": "Puppy K wk 1", "PK2": "Puppy K wk 2", "PK3": "Puppy K wk 3", "PK4": "Puppy K wk 4",
        "F05A": "Foundation wk 5 article", "F13V": "Foundation wk 13 video", "F14V": "Foundation wk 14 video",
        "NOTES": "Your notes"}
def wk(code):
    if code in WEEK: return WEEK[code]
    return "Foundation wk " + code[1:].lstrip("0") if code.startswith("F") else code

TRACKS = [
  dict(id="focus", name="Focus & Connection", short="Focus",
       blurb="Build a dog who checks in with you, loves your hands, and wants to work.",
       drills=["name_game", "charge_clicker", "hand_target", "cookie_fingers", "find_scatter"]),
  dict(id="calm", name="Self-Control & Calm", short="Calm",
       blurb="Impulse control games: good things come from waiting and choosing well.",
       drills=["its_your_choice", "take_it", "leave_it", "crate_games", "mat_work"]),
  dict(id="body", name="Body Awareness", short="Body",
       blurb="Feet, back ends and new surfaces. Confidence and coordination for indoor days.",
       drills=["novel_surfaces", "feet", "shaping", "perch_work", "two_on_two_off"]),
  dict(id="life", name="Life Skills & Recall", short="Life skills",
       blurb="Being caught, being handled, settling, letting go, and coming when called (hallway edition).",
       drills=["collar_grab", "play_and_settle", "tug_and_out", "loose_leash_walking", "restrained_recall"]),
  dict(id="agility", name="Agility Foundations", short="Agility",
       blurb="Flatwork you can do in a living room: position, sends, and turning away from you.",
       drills=["circle_work", "send_to_target_plate", "flip_away", "lap_turn", "wrap"]),
]

GEAR = {
  "name_game": ["Treat pouch or a jar by the kitchen", "Kibble from today's meal"],
  "charge_clicker": ["Clicker (or a retractable pen click)", "Tiny soft treats"],
  "hand_target": ["Just your hand", "Plastic lid as a hand-held target"],
  "cookie_fingers": ["Soft treats you can hold between fingers", "Clear hallway"],
  "find_scatter": ["Kibble", "Rug or yoga mat to scatter on (easier on paws, slows the hunt)"],
  "its_your_choice": ["Small treats", "Somewhere to sit on the floor"],
  "take_it": ["Kibble", "A favourite toy"],
  "leave_it": ["Lidded food container", "Leash", "Toy on the floor"],
  "crate_games": ["Crate with the pad removed", "Tug toy for the exit"],
  "mat_work": ["Bath mat, towel or dog bed", "Kong or chew for longer stays"],
  "novel_surfaces": ["Flattened cardboard box", "Yoga mat or folded towel", "Squishy exercise mat"],
  "feet": ["Upside-down dog bowl", "Thick book", "Bottom stair"],
  "shaping": ["Pizza box or shallow cardboard box", "Two small books", "Clicker"],
  "perch_work": ["Upside-down washing tub or sturdy bowl", "Squeeze tube of soft food or peanut butter (xylitol-free)"],
  "two_on_two_off": ["Sturdy board or the bottom stair as the 'contact'", "Paper plate as a target"],
  "collar_grab": ["Flat collar", "Nail clippers (just to show, later)"],
  "play_and_settle": ["Short house leash", "Treats in a pocket, not in your hand"],
  "tug_and_out": ["Two equal tug toys (rolled tea towel works)", "Hallway to keep the game contained"],
  "loose_leash_walking": ["6 ft leash", "Treat pouch on your hip", "Longest hallway in the house"],
  "restrained_recall": ["A helper", "Hallway or basement run", "Very visible toy"],
  "circle_work": ["Kitchen chair or laundry basket to circle", "Spatula with peanut butter for small dogs"],
  "send_to_target_plate": ["Paper plate or plastic lid as target plate", "Hallway"],
  "flip_away": ["Treats in both hands", "Clear floor space"],
  "lap_turn": ["Cone, upside-down recycling bin or kitchen chair as the 'wing'", "Toy to throw"],
  "wrap": ["Recycling bin, laundry basket or chair as the obstacle", "Toy to throw"],
}

# Humans-only bonus, one per day per track
BONUS = {
 "focus": [
   dict(kind="Watch", title="See shaping in action", text="Watch a 12-week puppy learn to back onto an object. Notice exactly when the trainer clicks and how the criteria change.", link="https://youtu.be/CpA25qUBxiA"),
   dict(kind="Practise", title="Play the Shaping Game", text="One person leaves the room; the others pick a behaviour (turn on a lamp, sit on the floor). Click only, no words or pointing. You'll find out fast how much timing matters."),
   dict(kind="Make", title="Prep a week of treats", text="Cut cheese, cooked chicken or hot dogs into pea-sized pieces. Bag them in session-sized portions (5–8 per exercise) and freeze."),
   dict(kind="Move", title="Work on your balance", text="Stand on one foot for 30 seconds while you brush your teeth, then switch. Next, walk heel-to-toe down the hallway. Steady handlers make clearer cues."),
   dict(kind="Read", title="Learn your cue words", text="Pick one word each for 'Yes', 'Good', your release, and 'Here'. Write them on a sticky note for the fridge so everyone in the house uses the same ones."),
 ],
 "calm": [
   dict(kind="Bake", title="Bake pumpkin oat treats", text="Mix 1 cup oat flour, ½ cup plain pumpkin purée and 2 tbsp xylitol-free peanut butter. Roll, cut into small squares, bake at 350°F for about 20 minutes. Cool completely; keep refrigerated."),
   dict(kind="Move", title="Calm breathing break", text="Five slow breaths: in for 4, out for 6. Dogs read our body; a calm handler makes calm games easier."),
   dict(kind="Watch", title="Crate games video", text="A short video on helping a dog love its crate. Watch how fast the reward follows going in.", link="https://youtu.be/FQ7evQmSWYk"),
   dict(kind="Read", title="Boundary Games", text="A free guide from Absolute Dogs with games that test your dog's commitment to a mat or place.", link="https://absolutedog.s3-eu-west-1.amazonaws.com/NBN+Bootcamps/Resources/aD-BoundaryGames__v11-low.pdf"),
   dict(kind="Make", title="Fill and freeze Kongs", text="Stuff three Kongs with soaked kibble and a smear of plain yogurt or pumpkin, then freeze. Ready-made mat-time for the rest of the week."),
 ],
 "body": [
   dict(kind="Move", title="Work on your balance", text="Stand on a folded towel on one leg for 20 seconds each side. Feel what your dog feels on a wobbly surface."),
   dict(kind="Make", title="Build a perch", text="Find a sturdy upside-down tub or bowl. Glue a rubber shelf liner or yoga mat scrap to the top for grip. Test it with your own hand pressure before the dog uses it."),
   dict(kind="Watch", title="Strengthening for agility", text="Saved link on strengthening skills for agility dogs. Save any exercises that need equipment for later.", link="https://hubs.li/Q03DhCh40"),
   dict(kind="Bake", title="Lickable treat tube", text="Blend plain cottage cheese with a spoon of pumpkin and spoon it into a reusable squeeze pouch. Perfect for perch work. Keep it refrigerated."),
   dict(kind="Read", title="Trick ideas", text="Five tricks every dog should know: Middle, Toes, Retrieve, Tidy Away and Circling. Pick one for next week.", link="https://absolute-dogs.com/blogs/gamechangers/5-top-tricks-every-dog-should-know-training-for-fun-and-practical-real-life-skills"),
 ],
 "life": [
   dict(kind="Practise", title="Rehearse the vet hold", text="Practise the collar & body hold motion on a stuffed animal: one arm under the tummy, one under the neck. Smooth hands make the real thing easier."),
   dict(kind="Make", title="Make a tea-towel tug", text="Knot two old tea towels together into a braid with a handle loop at each end. Instant second toy for 'Out' trades."),
   dict(kind="Move", title="Brisk hallway laps", text="Walk the hallway at 'late for something' pace for 3 minutes, practising crisp 180° turns. That's the loose-leash rhythm."),
   dict(kind="Watch", title="Whisper training", text="Saved video on quiet, low-voice cueing.", link="https://vimeo.com/651673085/91eda2810a"),
   dict(kind="Read", title="Plan your recall rewards", text="List your dog's top 5 rewards in order. Save the top two for 'Here' only, so the recall cue stays special."),
 ],
 "agility": [
   dict(kind="Practise", title="Footwork without the dog", text="Walk the lap-turn pattern alone around a chair: back up, dog-side leg and arm back, wait, then step forward. Do it on both sides until it feels like a dance."),
   dict(kind="Watch", title="Circle work video", text="Watch circle work done well. Notice the dog's position at the handler's side on the curve.", link="https://youtu.be/6OHVdhE9DqY"),
   dict(kind="Read", title="Backside sends", text="What a backside send is and how it's taught. Good preview of where wraps lead.", link="https://www.oneminddogs.com/blog/what-is-a-backside-send-in-dog-agility-and-how-do-you-teach-it/"),
   dict(kind="Move", title="Work on your balance", text="Practise quick direction changes: three steps forward, pivot, three steps back. Agility handlers need nimble feet too."),
   dict(kind="Make", title="Make target plates", text="Cut three plastic lids or paper plates; add a strip of coloured tape so your dog can spot them on any floor."),
 ],
}

import re
CODE = re.compile(r"\s*\((?:F|PK)\d+[A-Z]?(?:[/,]\s*(?:F|PK)?\d+[A-Z]?)*\)|,?\s*\b(?:F|PK)\d+[A-Z]?\b(?=\))")
def clean(s):
    if not s: return s
    s = CODE.sub("", s)
    return re.sub(r"\s+([.,;:])", r"\1", s).strip()

ALTERNATES = {
  "focus": ["push_away_and_run", "yes_marker", "informal_recall_cue"],
  "calm": ["sit_and_stays", "door_waits"],
  "body": ["off", "between"],
  "life": ["collar_body_hold", "meet_and_greet", "recall_here_come"],
  "agility": ["around_cone", "blind_cross_flat"],
}
GEAR.update({
  "push_away_and_run": ["Clear hallway or open room", "Tug toy for when they catch you"],
  "yes_marker": ["Small treats", "Nothing else: just your voice"],
  "informal_recall_cue": ["Treats in a pocket", "A fun, silly voice"],
  "sit_and_stays": ["Small treats in an open hand", "Non-slip rug"],
  "door_waits": ["Any interior door or the crate door", "Leash for outside doors"],
  "off": ["Low ottoman, cushion or dog bed", "Kibble to toss"],
  "between": ["Treats in both hands", "Space to stand with feet apart"],
  "collar_body_hold": ["A calm moment (after a walk or meal)", "A helper with treats (optional)"],
  "meet_and_greet": ["A visitor who'll ignore the dog at first", "Kitchen chair", "Leash"],
  "recall_here_come": ["Your best rewards, saved for this", "Hallway or basement"],
  "around_cone": ["Upside-down recycling bin, big mixing bowl or cone", "Treats"],
  "blind_cross_flat": ["A helper to hold the dog", "Treat or toy in each hand", "Hallway"],
})
EXTRA_BONUS = [
  dict(kind="Make", title="Snuffle towel", text="Lay an old bath towel flat, sprinkle kibble, and roll it up loosely. Tie a loose knot. Ready for a calm sniffing break."),
  dict(kind="Move", title="Stretch with your dog nearby", text="Five minutes of gentle stretching: calves, hips, shoulders. Handlers who bend and turn a lot need loose hips too."),
]

def drill(i):
    s = S[i]
    prog = s.get("progressions", [])
    nxt = clean(prog[0]["text"]) if prog else None
    tips = [clean(t) for t in s.get("tips", []) if "Video:" not in t and "http" not in t and "notes say" not in t and "Why 'mugging'" not in t and "word you were" not in t]
    return dict(id=i, name=s["name"], purpose=s["purpose"], level=s["level"],
                cues=s.get("cues", []), steps=[clean(x) for x in s.get("how_to", [])[:7]], next=nxt,
                tip=(tips[0] if tips else None), gear=GEAR[i],
                source=", ".join(sorted({wk(c) for c in s["sources"]}, key=lambda x: (x.startswith("Your"), x))))

OUT = dict(tracks=[dict(id=t["id"], name=t["name"], short=t["short"], blurb=t["blurb"],
                        days=[dict(drill=drill(d), bonus=b) for d, b in zip(t["drills"], BONUS[t["id"]])],
                        alternates=[drill(a) for a in ALTERNATES[t["id"]]]) for t in TRACKS],
           bonusPool=[b for t in TRACKS for b in BONUS[t["id"]]] + EXTRA_BONUS)
for i, b in enumerate(OUT["bonusPool"]): b["id"] = f"b{i+1}"
for t in OUT["tracks"]:
    assert len(t["days"]) == 5
def write(path):
    for tr in OUT["tracks"]:
        for d in tr["days"] + [dict(drill=a) for a in tr["alternates"]]:
            if d["drill"]["id"] == "lap_turn": d["drill"]["img"] = "assets/lap-turn-week13.gif"
    json.dump(dict(version=2, dogProfile=dict(name="Sunny"), **OUT), open(path, "w"), indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print(json.dumps(OUT, ensure_ascii=False))
