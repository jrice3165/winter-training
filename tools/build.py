import json, csv, sys, os, shutil
sys.path.insert(0, os.path.dirname(__file__))
import data

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(OUT, exist_ok=True)
LEVEL = {1: "Start here", 2: "Building", 3: "Advanced"}
skills = {s["id"]: s for s in data.SKILLS}
src = {s[0]: dict(id=s[0], program=s[1], week=s[2], dates=s[3], file=s[4], kind=s[5]) for s in data.SOURCES}

def norm(s):
    d = dict(id=s["id"], name=s["name"], aka=s.get("aka", []), theme=s["category"],
             level=s["level"], level_label=LEVEL[s["level"]], programs=s["programs"],
             purpose=s["purpose"], cues=s.get("cues", []), equipment=s.get("equipment", []),
             how_to=s.get("how_to", []), progressions=s.get("progressions", []),
             examples=s.get("examples", []), success_criteria=s.get("success_criteria", []),
             troubleshooting=s.get("troubleshooting", []), tips=s.get("tips", []),
             prerequisites=s.get("prerequisites", []), builds_toward=s.get("builds_toward", []),
             sources=s["sources"], gaps=s.get("gaps", []))
    # reverse links
    d["unlocked_by"] = sorted({o["id"] for o in data.SKILLS if s["id"] in o.get("builds_toward", [])} - set(d["prerequisites"]))
    d["resources"] = [i for i, r in enumerate(data.RESOURCES) if s["id"] in r["related"]]
    return d

out_skills = [norm(s) for s in data.SKILLS]
themes = [dict(id=c, name=n, skills=[s["id"] for s in out_skills if s["theme"] == c],
               resources=[i for i, r in enumerate(data.RESOURCES) if r["theme"] == c]) for c, n in data.CATEGORIES]
db = dict(
    meta=dict(title="Dog Training Skill Library", version=1, generated="2026-11-23",
              notes="Built from Sundog Foundation class notes (2021-22), Puppy Kindergarten notes (2022), personal notes and external links. 'level': 1 start here, 2 building, 3 advanced."),
    themes=themes, skills=out_skills,
    cues=[dict(cue=c, meaning=m, alternates=a, sources=s) for c, m, a, s in data.CUES],
    glossary=[dict(term=t, definition=d, sources=s) for t, d, s in data.GLOSSARY],
    resources=[dict(id=i, **r) for i, r in enumerate(data.RESOURCES)],
    sources=list(src.values()),
)
with open(f"{OUT}/dog_training_skills.json", "w") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

# flat index for spreadsheets
with open(f"{OUT}/dog_training_skills_index.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "name", "theme", "level", "programs", "cues", "prerequisites", "builds_toward", "sources", "has_gaps"])
    tname = dict(data.CATEGORIES)
    for s in out_skills:
        w.writerow([s["id"], s["name"], tname[s["theme"]], s["level"], ";".join(s["programs"]), ";".join(s["cues"]),
                    ";".join(s["prerequisites"]), ";".join(s["builds_toward"]), ";".join(s["sources"]), "yes" if s["gaps"] else ""])

# ------------------------------------------------------------------ markdown
def srcl(ids):
    return ", ".join(ids)
def link(i):
    return f"[{skills[i]['name']}](#{i.replace('_','-')})"

L = ["# Dog Training Skill Library", "",
     "Your Sundog Foundation agility class notes (2021–22), Puppy Kindergarten notes (2022), personal notes and saved links, organized by theme and skill.",
     "",
     "**Levels:** 1 = start here · 2 = building · 3 = advanced. **Source codes:** `PK1–PK4` Puppy Kindergarten weeks; `F02–F18` Foundation weeks; `F05A` toy-drive article; `F13` lap-turn diagram; `F13V`/`F14V` videos; `NOTES` your own notes. Full list at the end.",
     "", "## Contents", ""]
for t in themes:
    L.append(f"**{dict(data.CATEGORIES)[t['id']]}**: " + " · ".join(link(i) for i in t["skills"]))
    L.append("")
L += ["Also: [Suggested learning path](#suggested-learning-path) · [Cue glossary](#cue-glossary) · [Terms](#terms) · [External resources](#external-resources) · [Sources](#sources) · [Gaps to fill](#gaps-to-fill)", ""]

for t in themes:
    L += ["---", "", f"## {dict(data.CATEGORIES)[t['id']]}", ""]
    for i in t["skills"]:
        s = next(x for x in out_skills if x["id"] == i)
        L.append(f'<a id="{i.replace("_","-")}"></a>')
        L.append(f"### {s['name']}")
        meta = [f"Level {s['level']} ({s['level_label']})", "Programs: " + ", ".join(s["programs"])]
        if s["cues"]: meta.append("Cues: " + ", ".join(f"'{c}'" for c in s["cues"]))
        if s["aka"]: meta.append("Also called: " + ", ".join(s["aka"]))
        L += ["*" + " · ".join(meta) + "*", "", s["purpose"], ""]
        if s["equipment"]: L += ["**You'll need:** " + "; ".join(s["equipment"]), ""]
        if s["prerequisites"]: L += ["**Before this:** " + ", ".join(link(p) for p in s["prerequisites"]), ""]
        if s["how_to"]:
            L.append("**How to**"); L += [f"{n}. {x}" for n, x in enumerate(s["how_to"], 1)]; L.append("")
        if s["progressions"]:
            L.append("**Progressions**"); L += [f"- `{p['source']}` {p['text']}" for p in s["progressions"]]; L.append("")
        for ex in s["examples"]:
            L.append(f"**Example: {ex['name']}** (`{ex['source']}`)"); L += [f"{n}. {x}" for n, x in enumerate(ex["steps"], 1)]; L.append("")
        if s["success_criteria"]:
            L.append("**What 'right' looks like**"); L += [f"- {x}" for x in s["success_criteria"]]; L.append("")
        if s["troubleshooting"]:
            L.append("**Troubleshooting**"); L += [f"- {x}" for x in s["troubleshooting"]]; L.append("")
        if s["tips"]:
            L.append("**Tips**"); L += [f"- {x}" for x in s["tips"]]; L.append("")
        if s["gaps"]:
            L += ["> ⚠️ " + g for g in s["gaps"]]; L.append("")
        if s["builds_toward"]: L += ["**Leads to:** " + ", ".join(link(p) for p in s["builds_toward"]), ""]
        if s["resources"]:
            L += ["**More:** " + " · ".join(f"[{data.RESOURCES[r]['title']}]({data.RESOURCES[r]['url']})" for r in s["resources"]), ""]
        L += [f"<sub>Sources: {srcl(s['sources'])}</sub>", ""]

# learning path (topological by level then prereqs)
L += ["---", "", "## Suggested learning path", "",
      "Skills ordered so prerequisites come first, grouped by level.", ""]
done, order = set(), []
pending = sorted(out_skills, key=lambda s: s["level"])
while pending:
    for s in pending:
        if all(p in done for p in s["prerequisites"]):
            order.append(s); done.add(s["id"]); pending.remove(s); break
for lv in (1, 2, 3):
    L.append(f"**Level {lv}: {LEVEL[lv]}**: " + " → ".join(link(s["id"]) for s in order if s["level"] == lv)); L.append("")

L += ["---", "", "## Cue glossary", "", "| Cue | Meaning | Alternatives | Source |", "|---|---|---|---|"]
L += [f"| {c} | {m} | {', '.join(a)} | {srcl(s)} |" for c, m, a, s in data.CUES]
L += ["", "## Terms", "", "| Term | Meaning | Source |", "|---|---|---|"]
L += [f"| {t} | {d} | {srcl(s)} |" for t, d, s in data.GLOSSARY]

L += ["", "---", "", "## External resources", ""]
for t in themes:
    if not t["resources"]: continue
    L.append(f"**{dict(data.CATEGORIES)[t['id']]}**")
    for r in t["resources"]:
        R = data.RESOURCES[r]
        flag = "" if R["verified"] else " *(not opened/checked)*"
        L.append(f"- [{R['title']}]({R['url']}) ({R['publisher']}). {R['summary']}{flag}")
    L.append("")

L += ["## Sources", "", "| Code | Program | Week | Dates | File |", "|---|---|---|---|---|"]
L += [f"| {s['id']} | {s['program']} | {s['week'] or ''} | {s['dates'] or ''} | {s['file']} |" for s in src.values()]
L += ["", "## Gaps to fill", ""]
L += [f"- {link(s['id'])}: " + " ".join(s["gaps"]) for s in out_skills if s["gaps"]]
L.append("")
with open(f"{OUT}/dog_training_handbook.md", "w") as f:
    f.write("\n".join(L))
print("ok", len(out_skills))
