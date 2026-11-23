"""Write the three separated resource sets into docs/.

  docs/sundog/            Sundog-only skill library (handbook, JSON, CSV)
  docs/personal-notes/    Your own notes, by skill
  docs/external-links/    Saved links from outside Sundog
  docs/combined/          The original mixed library (all three together)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import data, sundog_data
from build import build

ROOT = os.path.join(os.path.dirname(__file__), "..", "docs")

build(data, f"{ROOT}/combined", prefix="combined_",
      title="Dog Training Skill Library (combined)",
      intro="Everything together: Sundog class notes, your personal notes and outside links. See docs/sundog for the Sundog-only version.")

build(sundog_data, f"{ROOT}/sundog", prefix="sundog_",
      title="Sundog Agility: Skill Library",
      intro="Only material from Sundog Agility: Foundation class notes (Weeks 2–18, 2021–22), Puppy Kindergarten notes (Weeks 1–4, 2022), the Week 13 lap-turn diagram, the Week 13/14 videos, and the Week 5 toy-drive handout (Susan Garrett article distributed in class). Personal notes and outside links are kept separately.")

# ---- personal notes ----
os.makedirs(f"{ROOT}/personal-notes", exist_ok=True)
L = ["# Personal training notes", "",
     "Your own notes, separated from the Sundog class materials. Skills marked *(yours only)* don't appear in the Sundog library at all; the others are skills Sundog also teaches, with what *your* notes added.", ""]
for s in sundog_data.PERSONAL_SKILLS:
    only = s["sources"] == ["NOTES"]
    L.append(f"## {s['name']}" + ("  *(yours only)*" if only else ""))
    L.append("")
    L.append(s["purpose"]); L.append("")
    if only:
        if s.get("cues"): L += ["Cues: " + ", ".join(f"'{c}'" for c in s["cues"]), ""]
        L += [f"{i}. {x}" for i, x in enumerate(s.get("how_to", []), 1)] + [""]
        L += [f"- {t}" for t in s.get("tips", [])] + [""]
        L += [f"> {g}" for g in s.get("gaps", [])] + ([""] if s.get("gaps") else [])
    else:
        mine = [p["text"] for p in s.get("progressions", []) if p["source"] == "NOTES"]
        if mine:
            L += ["From your notes:"] + [f"- {m}" for m in mine] + [""]
        L += [f"> {g}" for g in s.get("gaps", [])] + ([""] if s.get("gaps") else [])
L += ["## Leave it & Take it: your methods", "",
      "- Drop a kibble far enough away that the dog can't easily get it, say 'leave it', and reward with a better treat from you. Slowly decrease the distance. Test: throw a good treat nearby, say 'leave it', and the dog comes to you instead.",
      "- On leash, walk past a good toy (or treat), say 'leave it' and keep going with gentle leash pressure. Test: off leash, walking close by.",
      "- Take it: drop a kibble and cover it with your hand; don't lift until they back away, then say 'take it'. Slowly extend the wait. Works with toys too.", "",
      "## Standing on weird things & rear-end awareness: your additions", "",
      "- Upside-down dog bowls work great; squishy exercise mats help balance. Lure front feet on with 'feet', later back feet only.",
      "- For pivots, a squeeze tube of soft dog food or peanut butter (xylitol-free) gives the dog something to lick while you step around.", ""]
open(f"{ROOT}/personal-notes/personal_notes.md", "w").write("\n".join(L))

# ---- external links ----
os.makedirs(f"{ROOT}/external-links", exist_ok=True)
L = ["# External links (not Sundog)", "", "Saved resources from outside the Sundog classes.", "",
     "| Title | Publisher | What it is | Link |", "|---|---|---|---|"]
for r in sundog_data.EXTERNAL_RESOURCES:
    note = r["summary"] + ("" if r["verified"] else " (not opened/checked)")
    L.append(f"| {r['title']} | {r['publisher']} | {note} | {r['url']} |")
open(f"{ROOT}/external-links/external_links.md", "w").write("\n".join(L) + "\n")
print("sundog skills:", len(sundog_data.SKILLS), "| personal-note skills:", len(sundog_data.PERSONAL_SKILLS), "| external links:", len(sundog_data.EXTERNAL_RESOURCES))
