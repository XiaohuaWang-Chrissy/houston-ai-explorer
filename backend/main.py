import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

data_path = Path(__file__).parent / "data" / "houston_data.json"
with open(data_path) as f:
    raw = json.load(f)

industries = {ind["NAICS_3digit"]: ind for ind in raw["industries"]}
industry_trends = {}
for row in raw["industry_trend"]:
    key = row["NAICS_3digit"]
    industry_trends.setdefault(key, []).append(row)
tier_trend = raw["tier_trend"]


@app.get("/api/industries")
def get_industries():
    return sorted(raw["industries"], key=lambda x: x["Industry"])


@app.get("/api/industry/{naics}")
def get_industry(naics: str):
    if naics not in industries:
        raise HTTPException(status_code=404, detail="Industry not found")
    return {
        "info": industries[naics],
        "trend": sorted(industry_trends.get(naics, []), key=lambda x: x["Year"]),
        "tier_trend": tier_trend,
    }
