# Winter Training — Project Architecture & Implementation Guide

## 1. Project Overview
This repository contains the frontend application and print-generation pipeline for **Winter Training**, a specialized 15-minute winter indoor canine training planner and daily companion.

---

## 2. Directory Structure
```
winter-training/
├── DESIGN.md                   # Brand visual guidelines, tokens, typography, and color rules
├── data/
│   └── training-curriculum.json # 5 themes, 25 daily drills, household equipment & bonus activities
├── src/
│   ├── components/
│   │   ├── HeaderNav.html      # Top navigation with printable trigger and handler profile badge
│   │   ├── ThemeSelector.html  # 5-track curriculum selector bar
│   │   ├── DailyDrillCard.html # Single 15-min drill card with household equipment and trainer tips
│   │   ├── HumanBonusCard.html # Companion human enrichment micro-activities
│   │   └── GearIdeas.html      # Household gear ideas and everyday item suggestions
│   ├── pages/
│   │   ├── index.html          # Main 5-Day Training Plan & Dashboard
│   │   └── printable.html      # Ink-optimized single-page Letter/A4 printable sheet
│   └── styles/
│       ├── tokens.css          # Earthy variables (no green: saddle leather, parchment, espresso)
│       └── print.css           # CSS @media print rules for guaranteed 1-page fit
└── README.md
```

---

## 3. Key Technical Specifications

### A. Print Styling Rules (`print.css`)
```css
@media print {
  @page {
    size: letter portrait;
    margin: 0.5in;
  }
  body {
    background: #FFFFFF !important;
    color: #000000 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .no-print, header, nav, footer, button.print-trigger {
    display: none !important;
  }
  .printable-page-container {
    page-break-after: avoid;
    page-break-inside: avoid;
    height: 100%;
    max-height: 10.2in;
    box-shadow: none !important;
    border: 1px solid #D6C8B7 !important;
  }
}
```

### B. State Management
- `activeThemeId`: Controls which of the 5 curriculum tracks is loaded into Days 1 through 5.
- `dogProfile`: `{ name: "Sunny", breed: "Golden Retriever", age: "3 yrs" }`.
- `activeDrills`: Array of 5 drills derived from the active theme in `training-curriculum.json`.

---

## 4. Design Guidelines Summary
- **Brand Identity**: Rebranded exclusively as **Winter Training** (replacing FrostPaws).
- **Color Constraint**: **Zero green.** Backgrounds are warm oatmeal/parchment (`#FBF8F5`), borders are sand (`#EBE3D8`), active buttons and badges are saddle leather (`#7A431D`), and typography is deep espresso (`#231B15`).
- **Pacing & Layout**: Exactly 1 focused drill per day (15 minutes). No timer widgets, no rep/pass counters, no grading pressure, and household items presented under "Household Gear Ideas".
