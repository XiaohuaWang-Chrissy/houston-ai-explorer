# Houston AI Exposure Explorer

An interactive tool that lets you select your industry and see how exposed it is to artificial intelligence — and how wages and employment in Houston have shifted from 2022 to 2025.

Built as a companion to a data journalism project investigating how AI is reshaping the Houston labor market.

---

## What It Does

- Select any 3-digit NAICS industry from the Houston metro area
- See a weighted AI exposure score and tier (High / Medium / Low)
- View wage and employment trends from 2022–2025
- Compare your industry against the three tier averages

---

## Data Sources

| Dataset | Source |
|---|---|
| AI Occupational Exposure Scores | [Anthropic Economic Index](https://www.anthropic.com/research/labor-market-impacts) |
| Industry–Occupation Crosswalk | [BLS Occupational Employment Statistics (OES) 2024](https://www.bls.gov/oes/) |
| Houston Wage & Employment Data | [Texas LMI QCEW](https://texaslmi.com/LMIbyCategory/QCEW) |

---

## Methodology

For each 3-digit NAICS industry, we computed a **weighted average AI exposure score** using BLS OES national employment data as weights:

```
Industry AI Score = Σ (occupation AI score × occupation employment) / total industry employment
```

Industries were then divided into three equal tiers (High / Medium / Low) using quantile-based binning. Wage and employment trends are drawn from the Texas QCEW for the Houston–Pasadena–The Woodlands metro area, private sector only, 2022–2025.

**Limitations:**
- 2025 data covers Q1–Q3 only
- OES occupation mix is national, not Houston-specific
- Tier averages weight all industries equally regardless of size

---

## Tech Stack

- **Frontend**: Svelte + Vite + Chart.js
- **Backend**: Python + FastAPI

---

## How to Run

**Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173`.

---

## About

This project was built in collaboration with **Claude (Anthropic)** as part of a data journalism class at the Craig Newmark Graduate School of Journalism. The analysis, reporting, and editorial judgments are the author's own.

*Data journalism by Xiaohua Wang. Built with [Claude](https://claude.ai/code).*
