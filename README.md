# Winter Training

A calm, 15-minute-a-day indoor dog training planner. Pick one theme for the week and you get one drill per day (Day 1–5), a humans-only bonus activity, household gear ideas, and a printable one-page sheet.

Plain HTML, CSS and JavaScript, with no build step and no dependencies.

## Run it locally

The app loads its curriculum from `data/training-curriculum.json`, so it needs to be served by a web server. Double-clicking `index.html` won't load the data.

From this folder, run either of these:

```bash
python3 -m http.server 8000      # macOS has Python 3 built in
# or
npx serve .
```

Then open http://localhost:8000.

## Demo online (GitHub Pages)

1. Push this repo to GitHub.
2. In the repo, go to **Settings → Pages → Build and deployment**, choose **Deploy from a branch**, then pick branch **main** and folder **/ (root)**.
3. After about a minute the app is live at `https://<your-username>.github.io/winter-training/`.

## Project layout

```
index.html                     Page shell
css/tokens.css                 Design tokens (colours, light/dark) from docs/DESIGN.md
css/app.css                    Layout and components
css/print.css                  One-page Letter printable sheet
js/app.js                      Theme picker, day view, printable sheet, saved dog name
data/training-curriculum.json  5 tracks × 5 drills + humans-only bonus activities
assets/                        Images (Week 13 lap-turn diagram)
docs/                          DESIGN.md, ARCHITECTURE.md, full 48-skill library (handbook + JSON)
tools/                         Python scripts that regenerate the curriculum from the skill library
```

## Editing the curriculum

- **Quick edits:** change `data/training-curriculum.json` directly.
- **Regenerate from the skill library:** edit `tools/data.py` (skills) or `tools/planner_data.py` (tracks, gear, bonuses), then run:

```bash
cd tools
python3 -c "import json,planner_data as p; json.dump(dict(version=1,dogProfile=dict(name='Sunny'),tracks=p.OUT['tracks']),open('../data/training-curriculum.json','w'),indent=2,ensure_ascii=False)"
```

If you regenerate, re-add `"img": "assets/lap-turn-week13.gif"` to the lap turn drill.

## Notes

- The dog's name, chosen theme and day are saved in the browser (localStorage).
- Design rule from DESIGN.md: no green anywhere.
- Curriculum source: Sundog Foundation agility class notes (2021–22), Puppy Kindergarten notes (2022), and personal notes.
