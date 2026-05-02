from flask import Flask, request, jsonify, render_template
import logging
import requests
import time
import math
import datetime

from geoparser import parse_geonames


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


_cache = {
    "eonet": {"data": None, "timestamp": 0},
    "usgs": {"data": None, "timestamp": 0},
    "weather": {},  
    "india_weather": {"data": None, "timestamp": 0},
}
CACHE_TTL = 120  
WEATHER_CACHE_TTL = 300  

INDIA_MONITORING_STATIONS = [
    {"name": "Mumbai", "lat": 19.08, "lon": 72.88, "region": "Maharashtra"},
    {"name": "Delhi", "lat": 28.70, "lon": 77.10, "region": "Delhi NCR"},
    {"name": "Chennai", "lat": 13.08, "lon": 80.27, "region": "Tamil Nadu"},
    {"name": "Kolkata", "lat": 22.57, "lon": 88.36, "region": "West Bengal"},
    {"name": "Bangalore", "lat": 12.97, "lon": 77.59, "region": "Karnataka"},
    {"name": "Hyderabad", "lat": 17.39, "lon": 78.49, "region": "Telangana"},
    {"name": "Ahmedabad", "lat": 23.02, "lon": 72.57, "region": "Gujarat"},
    {"name": "Jaipur", "lat": 26.91, "lon": 75.79, "region": "Rajasthan"},
    {"name": "Lucknow", "lat": 26.85, "lon": 80.95, "region": "Uttar Pradesh"},
    {"name": "Bhopal", "lat": 23.26, "lon": 77.41, "region": "Madhya Pradesh"},
    {"name": "Patna", "lat": 25.59, "lon": 85.14, "region": "Bihar"},
    {"name": "Bhubaneswar", "lat": 20.30, "lon": 85.82, "region": "Odisha"},
    {"name": "Guwahati", "lat": 26.14, "lon": 91.74, "region": "Assam"},
    {"name": "Thiruvananthapuram", "lat": 8.52, "lon": 76.94, "region": "Kerala"},
    {"name": "Chandigarh", "lat": 30.73, "lon": 76.78, "region": "Punjab/Haryana"},
    {"name": "Dehradun", "lat": 30.32, "lon": 78.03, "region": "Uttarakhand"},
    {"name": "Raipur", "lat": 21.25, "lon": 81.63, "region": "Chhattisgarh"},
    {"name": "Ranchi", "lat": 23.34, "lon": 85.31, "region": "Jharkhand"},
    {"name": "Srinagar", "lat": 34.08, "lon": 74.80, "region": "J&K"},
    {"name": "Port Blair", "lat": 11.67, "lon": 92.74, "region": "Andaman"},
    {"name": "Gangtok", "lat": 27.33, "lon": 88.62, "region": "Sikkim"},
    {"name": "Visakhapatnam", "lat": 17.69, "lon": 83.22, "region": "Andhra Pradesh"},
    {"name": "Nagpur", "lat": 21.15, "lon": 79.09, "region": "Central India"},
    {"name": "Shimla", "lat": 31.10, "lon": 77.17, "region": "Himachal Pradesh"},
]

WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def haversine(lat1, lon1, lat2, lon2):
    
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def classify_weather_severity(weather_code, temp, wind_speed, humidity, precip):
  
    alerts = []


    if weather_code in [95, 96, 99]:
        desc = WMO_CODES.get(weather_code, "Severe thunderstorm")
        if weather_code == 99:
            alerts.append(("red", "⛈️ Severe Thunderstorm", f"{desc} — Seek shelter immediately"))
        else:
            alerts.append(("orange", "⛈️ Thunderstorm", f"{desc} — Stay indoors"))

    if weather_code == 82:
        alerts.append(("orange", "🌧️ Violent Rain", "Violent rain showers — Flood risk"))

    if weather_code in [65, 67]:
        alerts.append(("orange", "🌧️ Heavy Rain", WMO_CODES.get(weather_code, "Heavy rain")))

    if weather_code in [75, 86]:
        alerts.append(("orange", "❄️ Heavy Snow", WMO_CODES.get(weather_code, "Heavy snowfall")))

    if weather_code in [56, 57, 66]:
        alerts.append(("yellow", "🧊 Freezing Conditions", WMO_CODES.get(weather_code, "Freezing precipitation")))

    if temp is not None:
        if temp >= 48:
            alerts.append(("red", "🔥 Extreme Heat", f"Temperature {temp}°C — Life-threatening heat"))
        elif temp >= 44:
            alerts.append(("orange", "🌡️ Severe Heat", f"Temperature {temp}°C — Heat stroke risk"))
        elif temp >= 40:
            alerts.append(("yellow", "☀️ Heat Advisory", f"Temperature {temp}°C — Stay hydrated"))

        if temp <= -15:
            alerts.append(("red", "🥶 Extreme Cold", f"Temperature {temp}°C — Frostbite risk"))
        elif temp <= -5:
            alerts.append(("orange", "❄️ Severe Cold", f"Temperature {temp}°C — Hypothermia risk"))

    if wind_speed is not None:
        if wind_speed >= 90:
            alerts.append(("red", "🌪️ Cyclonic Winds", f"Wind speed {wind_speed} km/h — Extremely dangerous"))
        elif wind_speed >= 62:
            alerts.append(("orange", "💨 Storm Winds", f"Wind speed {wind_speed} km/h — Structural damage risk"))
        elif wind_speed >= 40:
            alerts.append(("yellow", "💨 Strong Winds", f"Wind speed {wind_speed} km/h — Use caution"))

    if precip is not None:
        if precip >= 30:
            alerts.append(("red", "🌊 Extreme Rainfall", f"Precipitation {precip} mm — Flash flood risk"))
        elif precip >= 15:
            alerts.append(("orange", "🌧️ Heavy Rainfall", f"Precipitation {precip} mm — Flooding possible"))

    if temp is not None and humidity is not None:
        if temp >= 35 and humidity >= 70:
            alerts.append(("orange", "🥵 Dangerous Heat Index", f"{temp}°C with {humidity}% humidity — Heat exhaustion risk"))

    return alerts


def fetch_weather_data(lat, lon):
    """Fetch current weather from Open-Meteo API (free, no key needed)."""
    cache_key = f"{round(lat, 1)}_{round(lon, 1)}"
    now = time.time()

    if cache_key in _cache["weather"]:
        cached = _cache["weather"][cache_key]
        if (now - cached["timestamp"]) < WEATHER_CACHE_TTL:
            return cached["data"]

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,"
            f"wind_speed_10m,wind_gusts_10m,apparent_temperature"
            f"&timezone=auto"
        )
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        data = r.json()

        _cache["weather"][cache_key] = {"data": data, "timestamp": now}
        return data
    except Exception as e:
        logger.error(f"Open-Meteo fetch error: {e}")
        if cache_key in _cache["weather"]:
            return _cache["weather"][cache_key]["data"]
        return None


def get_weather_alerts_for_location(lat, lon, place_name="Unknown"):
    """Get weather alerts for a specific location."""
    weather_data = fetch_weather_data(lat, lon)
    if not weather_data or "current" not in weather_data:
        return None

    current = weather_data["current"]
    temp = current.get("temperature_2m")
    humidity = current.get("relative_humidity_2m")
    precip = current.get("precipitation")
    weather_code = current.get("weather_code", 0)
    wind_speed = current.get("wind_speed_10m")
    wind_gusts = current.get("wind_gusts_10m")
    apparent_temp = current.get("apparent_temperature")

    effective_wind = max(wind_speed or 0, (wind_gusts or 0) * 0.7)

    severity_alerts = classify_weather_severity(
        weather_code, temp, effective_wind, humidity, precip
    )

    weather_desc = WMO_CODES.get(weather_code, "Unknown")

    result = {
        "place_name": place_name,
        "latitude": lat,
        "longitude": lon,
        "current_weather": {
            "temperature": temp,
            "feels_like": apparent_temp,
            "humidity": humidity,
            "precipitation": precip,
            "weather_code": weather_code,
            "weather_description": weather_desc,
            "wind_speed": wind_speed,
            "wind_gusts": wind_gusts,
        },
        "alerts": [],
        "highest_severity": None,
    }

    for severity, alert_type, description in severity_alerts:
        result["alerts"].append({
            "severity": severity,
            "type": alert_type,
            "description": description,
            "place": place_name,
            "latitude": lat,
            "longitude": lon,
        })

    if result["alerts"]:
        severity_order = {"red": 3, "orange": 2, "yellow": 1}
        result["highest_severity"] = max(
            result["alerts"], key=lambda a: severity_order.get(a["severity"], 0)
        )["severity"]

    return result


def is_india_related(place_name, lat, lon):
    """Check if a place is in or near India."""
    name_lower = place_name.lower()
    india_keywords = [
        "india", "maharashtra", "rajasthan", "gujarat", "delhi",
        "mumbai", "chennai", "kolkata", "bangalore", "hyderabad",
        "tamil nadu", "kerala", "karnataka", "punjab", "uttar pradesh",
        "bihar", "odisha", "assam", "west bengal", "madhya pradesh",
        "andhra pradesh", "telangana", "chhattisgarh", "jharkhand",
        "uttarakhand", "himachal", "goa", "manipur", "meghalaya",
        "mizoram", "nagaland", "sikkim", "tripura", "arunachal",
        "jammu", "kashmir", "ladakh", "chandigarh", "puducherry",
        "andaman", "lakshadweep", "haryana",
    ]
    if any(kw in name_lower for kw in india_keywords):
        return True
    if 6.0 <= lat <= 37.0 and 68.0 <= lon <= 98.0:
        return True
    return False


def get_nearby_stations(lat, lon, radius_km=600):
    nearby_stations = []
    for station in INDIA_MONITORING_STATIONS:
        dist = haversine(lat, lon, station["lat"], station["lon"])
        if dist <= radius_km:
            nearby_stations.append({**station, "distance_km": round(dist, 1)})

    nearby_stations.sort(key=lambda s: s["distance_km"])

    all_alerts = []
    station_data = []

    for station in nearby_stations:
        result = get_weather_alerts_for_location(
            station["lat"], station["lon"], station["name"]
        )
        if result:
            station_info = {
                "name": station["name"],
                "region": station["region"],
                "lat": station["lat"],
                "lon": station["lon"],
                "distance_km": station["distance_km"],
                "weather": result["current_weather"],
                "severity": result["highest_severity"],
                "alert_count": len(result["alerts"]),
            }
            station_data.append(station_info)

            for alert in result["alerts"]:
                alert["region"] = station["region"]
                alert["distance_km"] = station["distance_km"]
                all_alerts.append(alert)

    severity_order = {"red": 3, "orange": 2, "yellow": 1}
    all_alerts.sort(key=lambda a: severity_order.get(a["severity"], 0), reverse=True)

    return {
        "stations": station_data,
        "alerts": all_alerts,
        "total_alerts": len(all_alerts),
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
    }

def fetch_eonet_events():
    now = time.time()
    if _cache["eonet"]["data"] and (now - _cache["eonet"]["timestamp"]) < CACHE_TTL:
        return _cache["eonet"]["data"]

    try:
        url = "https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=50"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        events = r.json().get("events", [])
        _cache["eonet"]["data"] = events
        _cache["eonet"]["timestamp"] = now
        return events
    except Exception as e:
        logger.error(f"EONET fetch error: {e}")
        return _cache["eonet"]["data"] or []


def fetch_usgs_earthquakes():
    now = time.time()
    if _cache["usgs"]["data"] and (now - _cache["usgs"]["timestamp"]) < CACHE_TTL:
        return _cache["usgs"]["data"]

    try:
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        features = r.json().get("features", [])
        _cache["usgs"]["data"] = features
        _cache["usgs"]["timestamp"] = now
        return features
    except Exception as e:
        logger.error(f"USGS fetch error: {e}")
        return _cache["usgs"]["data"] or []


def get_nearby_alerts(lat, lon, radius_km=500):
    alerts = []
    eonet_events = fetch_eonet_events()
    for event in eonet_events:
        title = event.get("title", "Unknown Event")
        category = event["categories"][0]["title"] if event.get("categories") else "Unknown"
        geometries = event.get("geometry", [])
        if not geometries:
            continue

        latest = geometries[-1]
        coords = latest.get("coordinates")
        if not coords or len(coords) < 2:
            continue

        event_lon, event_lat = coords[0], coords[1]
        dist = haversine(lat, lon, event_lat, event_lon)

        if dist <= radius_km:
            alerts.append({
                "source": "NASA EONET",
                "title": title,
                "category": category,
                "distance_km": round(dist, 1),
                "latitude": round(event_lat, 4),
                "longitude": round(event_lon, 4),
                "date": latest.get("date", ""),
            })

    quakes = fetch_usgs_earthquakes()
    for quake in quakes:
        props = quake.get("properties", {})
        geom = quake.get("geometry", {})
        coords = geom.get("coordinates", [])

        if len(coords) < 2:
            continue

        q_lon, q_lat = coords[0], coords[1]
        dist = haversine(lat, lon, q_lat, q_lon)

        if dist <= radius_km:
            mag = props.get("mag", 0)
            timestamp = props.get("time", 0)
            date_str = ""
            if timestamp:
                date_str = datetime.datetime.fromtimestamp(
                    timestamp / 1000, tz=datetime.timezone.utc
                ).strftime("%Y-%m-%d %H:%M UTC")

            alerts.append({
                "source": "USGS",
                "title": props.get("title", f"M{mag} Earthquake"),
                "category": "Earthquake",
                "distance_km": round(dist, 1),
                "latitude": round(q_lat, 4),
                "longitude": round(q_lon, 4),
                "date": date_str,
                "magnitude": mag
            })

    alerts.sort(key=lambda x: x["distance_km"])
    return alerts[:15]  

@app.route("/")
def home():
    """Serve the main HTML interface."""
    return render_template("index.html")


@app.route("/parse", methods=["POST"])
def parse():
    """Parse geospatial entities from a sentence."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request body must be valid JSON"
            }), 400

        sentence = data.get("sentence", "").strip()

        if not sentence:
            return jsonify({
                "success": False,
                "error": "No sentence provided. Please provide a 'sentence' field."
            }), 400

        logger.info(f"Parsing sentence: {sentence}")
        results = parse_geonames(sentence)

        has_india = any(
            is_india_related(r["canonical_name"], r["latitude"], r["longitude"])
            for r in results
        )

        return jsonify({
            "success": True,
            "sentence": sentence,
            "results": results,
            "count": len(results),
            "has_india": has_india,
            "message": f"Successfully parsed {len(results)} geospatial entities"
        }), 200

    except Exception as e:
        logger.error(f"Error parsing sentence: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.route("/alerts", methods=["POST"])
def alerts():
    """Get real-time satellite alerts near a location."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "Invalid JSON"}), 400

        lat = data.get("latitude")
        lon = data.get("longitude")
        place = data.get("place_name", "Unknown")

        if lat is None or lon is None:
            return jsonify({"success": False, "error": "latitude and longitude required"}), 400

        logger.info(f"Fetching alerts near {place} ({lat}, {lon})")
        nearby = get_nearby_alerts(lat, lon, radius_km=500)

        return jsonify({
            "success": True,
            "place": place,
            "alerts": nearby,
            "count": len(nearby),
            "radius_km": 500
        }), 200

    except Exception as e:
        logger.error(f"Error fetching alerts: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Error fetching alerts: {str(e)}"
        }), 500


@app.route("/weather-alerts", methods=["POST"])
def weather_alerts():
    """Get real-time weather alerts for a specific location."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Invalid JSON"}), 400

        lat = data.get("latitude")
        lon = data.get("longitude")
        place = data.get("place_name", "Unknown")

        if lat is None or lon is None:
            return jsonify({"success": False, "error": "latitude and longitude required"}), 400

        logger.info(f"Fetching weather alerts for {place} ({lat}, {lon})")
        result = get_weather_alerts_for_location(lat, lon, place)

        if not result:
            return jsonify({
                "success": False,
                "error": "Could not fetch weather data"
            }), 500

        return jsonify({
            "success": True,
            **result
        }), 200

    except Exception as e:
        logger.error(f"Error fetching weather alerts: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Error: {str(e)}"
        }), 500


@app.route("/nearby-weather", methods=["POST"])
def nearby_weather():
    """Get weather for monitoring stations near a searched location."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Invalid JSON"}), 400

        lat = data.get("latitude")
        lon = data.get("longitude")
        place = data.get("place_name", "Unknown")

        if lat is None or lon is None:
            return jsonify({"success": False, "error": "lat/lon required"}), 400

        is_india = is_india_related(place, lat, lon)
        radius = 600 if is_india else 300

        logger.info(f"Fetching nearby weather for {place} (radius={radius}km)")
        result = get_nearby_stations(lat, lon, radius_km=radius)

        return jsonify({
            "success": True,
            "is_india": is_india,
            **result
        }), 200

    except Exception as e:
        logger.error(f"Error fetching nearby weather: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Error: {str(e)}"
        }), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Geospatial Query Engine"
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
