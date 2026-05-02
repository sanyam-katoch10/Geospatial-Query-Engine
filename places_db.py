
# ─── Countries ───────────────────────────────────────────────────────
COUNTRIES = {
    "afghanistan": (33.94, 67.71), "albania": (41.15, 20.17),
    "algeria": (28.03, 1.66), "argentina": (-38.42, -63.62),
    "australia": (-25.27, 133.78), "austria": (47.52, 14.55),
    "bangladesh": (23.69, 90.36), "belgium": (50.50, 4.47),
    "brazil": (-14.24, -51.93), "canada": (56.13, -106.35),
    "chile": (-35.68, -71.54), "china": (35.86, 104.20),
    "colombia": (4.57, -74.30), "cuba": (21.52, -77.78),
    "czech republic": (49.82, 15.47), "denmark": (56.26, 9.50),
    "egypt": (26.82, 30.80), "ethiopia": (9.15, 40.49),
    "finland": (61.92, 25.75), "france": (46.23, 2.21),
    "germany": (51.17, 10.45), "ghana": (7.37, -1.58),
    "greece": (39.07, 21.82), "hungary": (47.16, 19.50),
    "india": (20.59, 78.96), "indonesia": (-0.79, 113.92),
    "iran": (32.43, 53.69), "iraq": (33.31, 44.36),
    "ireland": (53.41, -8.24), "israel": (31.05, 34.85),
    "italy": (41.87, 12.57), "japan": (36.20, 138.25),
    "jordan": (30.59, 36.24), "kenya": (-0.02, 37.91),
    "kuwait": (29.31, 47.48), "malaysia": (4.21, 101.70),
    "mexico": (23.63, -102.55), "morocco": (31.79, -7.09),
    "myanmar": (21.92, 95.96), "nepal": (28.39, 84.12),
    "netherlands": (52.13, 5.29), "new zealand": (-40.90, 174.89),
    "nigeria": (9.08, 8.68), "north korea": (40.34, 127.51),
    "norway": (60.47, 8.47), "oman": (21.47, 55.98),
    "pakistan": (30.38, 69.35), "peru": (-9.19, -75.02),
    "philippines": (12.88, 121.77), "poland": (51.92, 19.15),
    "portugal": (39.40, -8.22), "qatar": (25.35, 51.18),
    "romania": (45.94, 24.97), "russia": (61.52, 105.32),
    "saudi arabia": (23.89, 45.08), "singapore": (1.35, 103.82),
    "south africa": (-30.56, 22.94), "south korea": (35.91, 127.77),
    "spain": (40.46, -3.75), "sri lanka": (7.87, 80.77),
    "sweden": (60.13, 18.64), "switzerland": (46.82, 8.23),
    "syria": (34.80, 38.10), "taiwan": (23.70, 120.96),
    "thailand": (15.87, 100.99), "turkey": (38.96, 35.24),
    "ukraine": (48.38, 31.17), "united arab emirates": (23.42, 53.85),
    "united kingdom": (55.38, -3.44), "united states": (37.09, -95.71),
    "venezuela": (6.42, -66.59), "vietnam": (14.06, 108.28),
    "zimbabwe": (-19.02, 29.15),
}

# ─── States / Provinces ─────────────────────────────────────────────
# India - All 28 states + 8 Union Territories
STATES = {
    # Indian States
    "andhra pradesh": (15.91, 78.67), "arunachal pradesh": (28.22, 94.73),
    "assam": (26.14, 91.77), "bihar": (25.10, 85.31),
    "chhattisgarh": (21.28, 81.87), "goa": (15.30, 73.82),
    "gujarat": (22.26, 71.19), "haryana": (29.06, 76.08),
    "himachal pradesh": (31.74, 77.12), "jharkhand": (23.61, 85.28),
    "karnataka": (15.32, 75.71), "kerala": (10.85, 76.27),
    "madhya pradesh": (22.97, 78.66), "maharashtra": (19.75, 75.71),
    "manipur": (24.66, 93.91), "meghalaya": (25.47, 91.37),
    "mizoram": (23.16, 92.94), "nagaland": (26.16, 94.56),
    "odisha": (20.95, 85.10), "punjab": (31.15, 75.34),
    "rajasthan": (27.02, 74.22), "sikkim": (27.53, 88.51),
    "tamil nadu": (11.13, 79.28), "telangana": (18.11, 79.02),
    "tripura": (23.94, 91.99), "uttar pradesh": (26.85, 80.95),
    "uttarakhand": (30.07, 79.02), "west bengal": (24.52, 88.23),
    # Indian Union Territories
    "delhi": (28.70, 77.10), "jammu and kashmir": (33.78, 76.58),
    "ladakh": (34.15, 77.58), "chandigarh": (30.73, 76.78),
    "puducherry": (12.07, 79.87),
    "andaman and nicobar islands": (11.74, 92.66),
    "dadra and nagar haveli": (20.18, 73.05),
    "daman and diu": (20.63, 72.85), "lakshadweep": (10.57, 72.74),

    # USA - Major States
    "california": (36.78, -119.42), "texas": (31.97, -99.90),
    "florida": (27.66, -81.52), "new york state": (43.30, -74.22),
    "pennsylvania": (41.20, -77.19), "illinois": (40.63, -89.40),
    "ohio": (40.42, -82.91), "georgia state": (32.16, -82.90),
    "north carolina": (35.76, -79.02), "michigan": (44.31, -85.60),
    "new jersey": (40.06, -74.41), "virginia": (37.43, -78.66),
    "washington state": (47.75, -120.74), "arizona": (34.05, -111.09),
    "massachusetts": (42.41, -71.38), "tennessee": (35.52, -86.58),
    "colorado": (39.55, -105.78), "maryland": (39.05, -76.64),
    "minnesota": (46.73, -94.69), "wisconsin": (43.78, -88.79),
    "alabama": (32.32, -86.90), "louisiana": (30.98, -91.96),
    "kentucky": (37.84, -84.27), "oregon": (43.80, -120.55),
    "connecticut": (41.60, -72.90), "utah": (39.32, -111.09),
    "nevada": (38.80, -116.42), "hawaii": (19.90, -155.58),
    "alaska": (64.20, -152.49), "indiana": (40.27, -86.13),

    # China - Major Provinces
    "guangdong": (23.13, 113.27), "zhejiang": (29.18, 120.08),
    "jiangsu": (32.97, 119.45), "shandong": (36.67, 116.99),
    "sichuan": (30.57, 104.07), "hubei": (30.59, 114.34),
    "hunan": (27.61, 111.71), "henan": (34.77, 113.72),
    "fujian": (26.10, 119.30), "hebei": (38.04, 114.51),
    "liaoning": (41.80, 123.43), "yunnan": (25.04, 102.71),
    "shaanxi": (34.26, 108.94), "xinjiang": (43.79, 87.63),
    "tibet": (29.65, 91.10), "inner mongolia": (40.82, 111.77),

    # UK - Nations
    "england": (52.36, -1.17), "scotland": (56.49, -4.20),
    "wales": (52.13, -3.78), "northern ireland": (54.79, -6.49),

    # Australia - States & Territories
    "new south wales": (-33.87, 151.21), "victoria": (-37.81, 144.96),
    "queensland": (-20.92, 142.70), "western australia": (-31.95, 115.86),
    "south australia": (-34.93, 138.60), "tasmania": (-42.88, 147.33),
    "northern territory": (-12.46, 130.84),

    # Canada - Provinces
    "ontario": (51.25, -85.32), "quebec": (52.94, -73.55),
    "british columbia": (53.73, -127.65), "alberta": (53.93, -116.58),
    "manitoba": (53.76, -98.81), "saskatchewan": (52.94, -106.45),
    "nova scotia": (44.68, -63.74),

    # Pakistan - Provinces
    "sindh": (25.89, 68.52), "balochistan": (28.49, 65.10),
    "khyber pakhtunkhwa": (34.95, 72.33),
    "punjab province": (31.17, 72.71),

    # Japan - Key Regions
    "hokkaido": (43.06, 141.35), "osaka prefecture": (34.69, 135.50),
    "kyoto prefecture": (35.01, 135.77), "aichi": (35.18, 136.91),

    # Germany - Key States
    "bavaria": (48.79, 11.50), "hesse": (50.65, 9.16),
    "saxony": (51.10, 13.20), "north rhine-westphalia": (51.43, 7.66),

    # Brazil - Key States
    "sao paulo state": (-23.55, -46.63), "rio de janeiro state": (-22.91, -43.17),
    "minas gerais": (-18.51, -44.56), "bahia": (-12.58, -41.70),
}

# ─── Cities ──────────────────────────────────────────────────────────
CITIES = {
    # ── India: Major Cities ──
    "mumbai": (19.08, 72.88), "delhi": (28.70, 77.10),
    "bangalore": (12.97, 77.59), "hyderabad": (17.39, 78.49),
    "ahmedabad": (23.02, 72.57), "chennai": (13.08, 80.27),
    "kolkata": (22.57, 88.36), "surat": (21.17, 72.83),
    "pune": (18.52, 73.86), "jaipur": (26.91, 75.79),
    "lucknow": (26.85, 80.95), "kanpur": (26.45, 80.33),
    "nagpur": (21.15, 79.09), "indore": (22.72, 75.86),
    "thane": (19.22, 72.98), "bhopal": (23.26, 77.41),
    "visakhapatnam": (17.69, 83.22), "patna": (25.59, 85.14),
    "vadodara": (22.31, 73.18), "ghaziabad": (28.67, 77.45),
    "ludhiana": (30.90, 75.86), "agra": (27.18, 78.01),
    "nashik": (20.00, 73.79), "faridabad": (28.41, 77.32),
    "meerut": (28.98, 77.71), "rajkot": (22.30, 70.80),
    "varanasi": (25.32, 82.99), "srinagar": (34.08, 74.80),
    "aurangabad": (19.88, 75.34), "dhanbad": (23.80, 86.43),
    "amritsar": (31.63, 74.87), "navi mumbai": (19.03, 73.03),
    "allahabad": (25.44, 81.85), "ranchi": (23.34, 85.31),
    "howrah": (22.60, 88.26), "coimbatore": (11.00, 76.91),
    "jabalpur": (23.18, 79.99), "gwalior": (26.22, 78.16),
    "vijayawada": (16.51, 80.65), "jodhpur": (26.24, 73.02),
    "madurai": (9.93, 78.12), "raipur": (21.25, 81.63),
    "kota": (25.21, 75.86), "chandigarh": (30.73, 76.78),
    "guwahati": (26.14, 91.74), "solapur": (17.66, 75.91),
    "mysore": (12.30, 76.64), "bareilly": (28.37, 79.43),
    "bhubaneswar": (20.30, 85.82), "kochi": (9.93, 76.27),
    "dehradun": (30.32, 78.03), "jamshedpur": (22.80, 86.18),
    "noida": (28.54, 77.39), "bikaner": (28.02, 73.31),
    "udaipur": (24.59, 73.71), "mangalore": (12.86, 74.84),
    "ajmer": (26.45, 74.64), "kolhapur": (16.70, 74.23),
    "jammu": (32.73, 74.86), "belgaum": (15.86, 74.50),
    "thiruvananthapuram": (8.52, 76.94), "tiruchirappalli": (10.79, 78.70),
    "salem": (11.66, 78.15), "warangal": (17.97, 79.59),
    "guntur": (16.31, 80.44),
    # India: More Tier-2/3 Cities
    "shimla": (31.10, 77.17), "manali": (32.24, 77.19),
    "haridwar": (29.95, 78.16), "rishikesh": (30.09, 78.27),
    "varanasi": (25.32, 83.01), "mathura": (27.49, 77.67),
    "gorakhpur": (26.76, 83.37), "aligarh": (27.88, 78.08),
    "moradabad": (28.84, 78.78), "saharanpur": (29.97, 77.55),
    "muzaffarpur": (26.12, 85.39), "bhagalpur": (25.24, 86.97),
    "gaya": (24.80, 85.00), "durgapur": (23.52, 87.32),
    "siliguri": (26.73, 88.42), "asansol": (23.69, 86.96),
    "cuttack": (20.46, 85.88), "rourkela": (22.26, 84.85),
    "tirupati": (13.63, 79.42), "nellore": (14.44, 79.97),
    "kakinada": (16.96, 82.24), "rajahmundry": (16.99, 81.80),
    "vellore": (12.92, 79.13), "thanjavur": (10.79, 79.14),
    "tirunelveli": (8.73, 77.70), "tuticorin": (8.76, 78.13),
    "erode": (11.34, 77.73), "dindigul": (10.37, 77.98),
    "kozhikode": (11.25, 75.77), "thrissur": (10.53, 76.21),
    "palakkad": (10.78, 76.65), "kannur": (11.87, 75.37),
    "kollam": (8.89, 76.61), "alappuzha": (9.49, 76.34),
    "hubli": (15.36, 75.12), "davanagere": (14.46, 75.92),
    "bellary": (15.14, 76.92), "hassan": (13.01, 76.10),
    "udupi": (13.34, 74.75), "panaji": (15.50, 73.83),
    "margao": (15.28, 73.96), "gangtok": (27.33, 88.62),
    "shillong": (25.57, 91.88), "imphal": (24.82, 93.95),
    "aizawl": (23.73, 92.72), "kohima": (25.67, 94.11),
    "itanagar": (27.08, 93.61), "agartala": (23.83, 91.29),
    "port blair": (11.67, 92.74), "dharamshala": (32.22, 76.32),
    "nainital": (29.38, 79.45), "mussoorie": (30.45, 78.07),
    "haldwani": (29.22, 79.51), "roorkee": (29.87, 77.89),
    "bilaspur": (22.09, 82.15), "korba": (22.35, 82.68),
    "jhansi": (25.45, 78.57), "ujjain": (23.18, 75.78),

    # ── USA: Major Cities ──
    "new york": (40.71, -74.01), "los angeles": (34.05, -118.24),
    "chicago": (41.88, -87.63), "houston": (29.76, -95.37),
    "phoenix": (33.45, -112.07), "philadelphia": (39.95, -75.17),
    "san antonio": (29.42, -98.49), "san diego": (32.72, -117.16),
    "dallas": (32.78, -96.80), "san jose": (37.34, -121.89),
    "austin": (30.27, -97.74), "washington": (38.91, -77.04),
    "boston": (42.36, -71.06), "seattle": (47.61, -122.33),
    "denver": (39.74, -104.99), "nashville": (36.16, -86.78),
    "miami": (25.76, -80.19), "atlanta": (33.75, -84.39),
    "san francisco": (37.77, -122.42), "las vegas": (36.17, -115.14),
    "detroit": (42.33, -83.05), "portland": (45.52, -122.68),
    "minneapolis": (44.98, -93.27),

    # ── China: Major Cities ──
    "beijing": (39.90, 116.41), "shanghai": (31.23, 121.47),
    "guangzhou": (23.13, 113.26), "shenzhen": (22.54, 114.06),
    "chengdu": (30.57, 104.07), "wuhan": (30.59, 114.31),
    "hangzhou": (30.27, 120.15), "nanjing": (32.06, 118.80),
    "chongqing": (29.43, 106.91), "tianjin": (39.13, 117.20),
    "xi'an": (34.26, 108.94), "suzhou": (31.30, 120.59),

    # ── UK: Major Cities ──
    "london": (51.51, -0.13), "manchester": (53.48, -2.24),
    "birmingham": (52.49, -1.90), "liverpool": (53.41, -2.98),
    "edinburgh": (55.95, -3.19), "glasgow": (55.86, -4.25),
    "bristol": (51.45, -2.59), "cardiff": (51.48, -3.18),
    "belfast": (54.60, -5.93), "leeds": (53.80, -1.55),

    # ── Japan: Major Cities ──
    "tokyo": (35.68, 139.65), "osaka": (34.69, 135.50),
    "kyoto": (35.01, 135.77), "yokohama": (35.44, 139.64),
    "nagoya": (35.18, 136.91), "sapporo": (43.06, 141.35),
    "kobe": (34.69, 135.20), "fukuoka": (33.59, 130.40),
    "hiroshima": (34.40, 132.46),

    # ── Australia: Major Cities ──
    "sydney": (-33.87, 151.21), "melbourne": (-37.81, 144.96),
    "brisbane": (-27.47, 153.03), "perth": (-31.95, 115.86),
    "adelaide": (-34.93, 138.60), "canberra": (-35.28, 149.13),

    # ── Canada: Major Cities ──
    "toronto": (43.65, -79.38), "vancouver": (49.28, -123.12),
    "montreal": (45.50, -73.57), "calgary": (51.05, -114.07),
    "ottawa": (45.42, -75.70), "edmonton": (53.55, -113.49),

    # ── Europe: Key Cities ──
    "paris": (48.86, 2.35), "berlin": (52.52, 13.41),
    "madrid": (40.42, -3.70), "rome": (41.90, 12.50),
    "amsterdam": (52.37, 4.90), "vienna": (48.21, 16.37),
    "zurich": (47.38, 8.54), "brussels": (50.85, 4.35),
    "prague": (50.08, 14.42), "stockholm": (59.33, 18.07),
    "lisbon": (38.72, -9.14), "dublin": (53.35, -6.26),
    "moscow": (55.76, 37.62), "istanbul": (41.01, 28.98),
    "athens": (37.98, 23.73), "barcelona": (41.39, 2.17),
    "munich": (48.14, 11.58), "milan": (45.46, 9.19),

    # ── Middle East ──
    "dubai": (25.20, 55.27), "abu dhabi": (24.45, 54.65),
    "riyadh": (24.71, 46.68), "doha": (25.29, 51.53),
    "tehran": (35.69, 51.39), "baghdad": (33.31, 44.37),
    "cairo": (30.04, 31.24), "amman": (31.95, 35.93),
    "muscat": (23.61, 58.54), "kuwait city": (29.38, 47.99),

    # ── South Asia / SE Asia ──
    "karachi": (24.86, 67.00), "lahore": (31.55, 74.35),
    "islamabad": (33.69, 73.04), "dhaka": (23.81, 90.41),
    "colombo": (6.93, 79.84), "kathmandu": (27.72, 85.32),
    "kabul": (34.52, 69.17), "bangkok": (13.76, 100.50),
    "hanoi": (21.03, 105.85), "ho chi minh city": (10.82, 106.63),
    "kuala lumpur": (3.14, 101.69), "jakarta": (-6.21, 106.85),
    "manila": (14.60, 120.98), "singapore": (1.35, 103.82),
    "yangon": (16.87, 96.20),

    # ── Africa ──
    "nairobi": (-1.29, 36.82), "lagos": (6.52, 3.38),
    "johannesburg": (-26.20, 28.04), "cape town": (-33.93, 18.42),
    "addis ababa": (9.02, 38.75), "accra": (5.56, -0.19),
    "casablanca": (33.57, -7.59), "dar es salaam": (-6.79, 39.28),

    # ── South America ──
    "sao paulo": (-23.55, -46.63), "rio de janeiro": (-22.91, -43.17),
    "buenos aires": (-34.60, -58.38), "bogota": (4.71, -74.07),
    "lima": (-12.05, -77.04), "santiago": (-33.45, -70.67),
    "caracas": (10.48, -66.90),
}

ALL_TABLES = {
    "Country": COUNTRIES,
    "State": STATES,
    "City": CITIES
}


def get_coordinates(table_name, place_name):
    if table_name not in ALL_TABLES:
        return None
    table = ALL_TABLES[table_name]
    for name, coords in table.items():
        if name.lower() == place_name.lower():
            return coords
    return None


def get_all_places(table_name=None):
    if table_name:
        return {table_name: ALL_TABLES[table_name]} if table_name in ALL_TABLES else {}
    return ALL_TABLES
