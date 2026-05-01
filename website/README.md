# ClearVision — Suspect Search Prototype

Police suspect search system: upload a suspect photo, select a city and date/time range, and scan all simulated CCTV cameras in that area.

## Quick Start

```bash
cd website/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

Open browser: http://localhost:8080

## Usage

1. Login with any username/password
2. Upload a suspect photo (any image)
3. Select city (Bangalore, Mumbai, Delhi, Chennai, Hyderabad)
4. Set date/time range (or use quick intervals: Last 1hr / 6hr / 24hr / 48hr)
5. Click **SCAN ALL CCTVs**
6. View results on map — red pulsing markers = matches, blue dots = all cameras
7. Click a timeline entry to jump to that camera on the map
8. Click **Export Report** to download a text report

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Login page |
| GET | `/dashboard` | Dashboard |
| GET | `/api/cities` | List of cities |
| GET | `/api/cameras?city=Bangalore` | All cameras for a city |
| POST | `/api/search` | Search (photo + city + datetime range) |
| GET | `/health` | Health check |
