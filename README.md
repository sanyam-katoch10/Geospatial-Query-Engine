# Geospatial Query Engine

A natural language processing system that identifies geospatial entities (place names) from user queries with intelligent fuzzy matching to handle spelling variations and provide canonical names.

## Features

- Extracts geographic entities using spaCy NLP (recognizes GPE and LOC entities)
- Handles spelling variations and typos (e.g., "Indya" → "India", "Londan" → "London")
- Supports three geographic levels: Countries, States, and Cities
- Interactive map visualization with Leaflet
- Real-time satellite alerts from NASA EONET and USGS Earthquake feeds
- Street and satellite map layer toggle

## Installation

```bash
# Install required Python packages
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

## Usage

### Run the Web Interface

```bash
python app.py
```

Then open http://localhost:5000 in your browser.

### Test Core Logic

```bash
python geoparser.py
```

## API Endpoints

**POST `/parse`** — Parse geospatial entities from a sentence

```json
{
  "sentence": "Which cities are in Maharashtra and what is their weather?"
}
```

**POST `/alerts`** — Get real-time satellite alerts near a location

```json
{
  "latitude": 19.7515,
  "longitude": 75.7139,
  "place_name": "maharashtra"
}
```

**GET `/health`** — Health check

## System Architecture

- **`geoparser.py`** — Core NLP extraction + fuzzy matching engine
- **`places_db.py`** — Canonical database with coordinates (67 countries, 37 states, 144 cities)
- **`app.py`** — Flask server with parse, alerts, and health endpoints
- **`templates/index.html`** — Web UI with map visualization

## Data Sources

- **Place database**: Hardcoded canonical names with lat/lon coordinates
- **Satellite alerts**: NASA EONET (natural events) + USGS (earthquakes), fetched in real-time

## Configuration

Adjust `MATCH_THRESHOLD` in `geoparser.py` to control fuzzy matching strictness:
- **72** (default): Good balance between catching misspellings and avoiding false positives
- **80+**: Stricter matching
- **60-70**: More permissive

## Requirements

- flask — Web framework
- rapidfuzz — Fuzzy string matching
- spacy — Natural Language Processing
- requests — HTTP client for satellite alert APIs
