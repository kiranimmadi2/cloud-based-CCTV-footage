from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random
import string
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from mock_data import get_cameras, generate_search_results, CITY_CENTERS, get_city_stats

app = FastAPI(title="ClearVision API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _new_case_id(city: str) -> str:
    prefix = city[:3].upper()
    year = datetime.now().year
    num = random.randint(1000, 9999)
    suffix = ''.join(random.choices(string.ascii_uppercase, k=2))
    return f"CASE-{year}-{prefix}-{num}{suffix}"


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "ClearVision", "version": "2.0"}


@app.get("/api/cities")
def cities():
    return {"cities": list(CITY_CENTERS.keys())}


@app.get("/api/cameras")
def cameras(city: str = "Bangalore"):
    cams = get_cameras(city)
    if not cams:
        raise HTTPException(status_code=404, detail=f"No cameras found for city: {city}")
    center = CITY_CENTERS.get(city, {"lat": 12.9716, "lng": 77.5946, "zoom": 12})
    stats = get_city_stats(city)
    return {
        "city": city,
        "center": center,
        "cameras": cams,
        "total": len(cams),
        "stats": stats,
    }


@app.get("/api/case")
def new_case(city: str = "Bangalore"):
    return {"case_id": _new_case_id(city)}


@app.post("/api/search")
async def search(
    photo: UploadFile = File(...),
    city: str = Form("Bangalore"),
    start_datetime: str = Form(...),
    end_datetime: str = Form(...),
    case_id: str = Form(""),
    priority: str = Form("HIGH"),
):
    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        start_dt = datetime.fromisoformat(start_datetime)
        end_dt = datetime.fromisoformat(end_datetime)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO 8601.")

    if end_dt <= start_dt:
        raise HTTPException(status_code=400, detail="End datetime must be after start datetime")

    results = generate_search_results(city, start_dt, end_dt)
    center = CITY_CENTERS.get(city, {"lat": 12.9716, "lng": 77.5946, "zoom": 12})
    case = case_id or _new_case_id(city)

    first_seen = results[0]["timestamp"] if results else None
    last_seen = results[-1]["timestamp"] if results else None
    top_conf = max((r["confidence"] for r in results), default=0)
    critical_count = sum(1 for r in results if r["alert_level"] == "CRITICAL")

    return {
        "status": "success",
        "case_id": case,
        "priority": priority,
        "city": city,
        "center": center,
        "total_cameras_scanned": len(get_cameras(city)),
        "matches_found": len(results),
        "top_confidence": round(top_conf, 2),
        "critical_hits": critical_count,
        "first_seen": first_seen,
        "last_seen": last_seen,
        "search_window": {
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
        },
        "results": results,
    }
