# Winter Training

A calm, 15-minute-a-day indoor dog training planner. Pick one theme for the week and you get one drill per day (Day 1–5), a humans-only bonus activity, household gear ideas, and a printable one-page sheet.

Don't like a day's drill? **Pick another drill** swaps in a different one from the same theme (each theme has 2–3 extra drills). **Pick another** on the bonus card does the same for the humans-only activity. Swaps are remembered per theme, and **Reset week** restores the original plan.

Plain HTML, CSS and JavaScript, with no build step and no dependencies.

## Two apps in this repo

| App | Folder | Content | Live |
|---|---|---|---|
| **Winter Training** | `/` (root) | Sundog class notes + personal notes + outside links (combined) | https://jrice3165.github.io/winter-training/ |
| **Sundog Winter Training (test)** | `/sundog` | Sundog Agility materials only, orange & blue theme | https://jrice3165.github.io/winter-training/sundog/ |

They share the same code; each has its own `data/training-curriculum.json`, `css/tokens.css` and saved settings.

## Resource sets (docs/)

| Folder | What's in it |
|---|---|
| `docs/sundog/` | Sundog-only skill library: handbook (Markdown), JSON, CSV index (41 skills) |
| `docs/personal-notes/` | Your own notes, separated out |
| `docs/external-links/` | Saved links from outside Sundog (Absolute Dogs, OneMind Dogs, etc.) |
| `docs/combined/` | The original mixed library |

Regenerate all of these with `python3 tools/split.py`. The Sundog app's curriculum comes from `tools/sundog_planner.py`:

```bash
cd tools
python3 -c "import sundog_planner as p; p.write('../sundog/data/training-curriculum.json')"
```

## Run it locally

The app loads its curriculum from `data/training-curriculum.json`, so it needs to be served by a web server. Double-clicking `index.html` won't load the data.

From this folder, run either of these:

```bash
python3 -m http.server 8000      # macOS has Python 3 built in
# or
npx serve .
```

Then open http://localhost:8000 (main app) or http://localhost:8000/sundog/ (Sundog test app).

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
data/training-curriculum.json  5 tracks × 5 drills (+ alternates) and a pool of humans-only bonuses
assets/                        Images (Week 13 lap-turn diagram)
docs/                          DESIGN.md, ARCHITECTURE.md, and the separated resource sets (see above)
sundog/                        Sundog Winter Training (test) app
tools/                         Python scripts: data.py (all skills), sundog_data.py (Sundog filter), split.py, planner builders
```

## Editing the curriculum

- **Quick edits:** change `data/training-curriculum.json` directly.
- **Regenerate from the skill library:** edit `tools/data.py` (skills) or `tools/planner_data.py` (tracks, alternates, gear, bonuses), then run:

```bash
cd tools
python3 -c "import planner_data as p; p.write('../data/training-curriculum.json')"
```

## Notes

- The dog's name, chosen theme and day are saved in the browser (localStorage).
- Design rule from DESIGN.md: no green anywhere.
- Curriculum source: Sundog Foundation agility class notes (2021–22), Puppy Kindergarten notes (2022), and personal notes.

## Releasing an update

When you change CSS or JS, bump the `?v=` number on the `<link>` and `<script>` tags in `index.html` (for example `?v=2` to `?v=3`). That makes browsers load the new files instead of a cached copy. The curriculum JSON is always re-checked.
