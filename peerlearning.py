"""
Welcome Uganda! -- Terminal-based Travel Guide (Full single-file version)
Features:
 - 30 attractions (A001..A030) with placeholder image filenames
 - View / search / filter (region/category)
 - Attraction details (auto-open image, open Google Maps)
 - Routes: CURRENT -> attraction, attraction -> attraction (with steps)
 - Reviews (anonymous option) with full date/time
 - Favorites (add / view / remove)
 - Exit confirmation, friendly emojis & prompts
"""

import json
import os
import subprocess
import platform
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from urllib.parse import quote_plus
import itertools

# ---------------- Paths ----------------
DATA_DIR = Path("data")
IMAGES_DIR = DATA_DIR / "images"
ATTRACTIONS_FILE = DATA_DIR / "attractions.json"
REVIEWS_FILE = DATA_DIR / "reviews.json"
FAVORITES_FILE = DATA_DIR / "favorites.json"
ROUTES_FILE = DATA_DIR / "routes.json"

# ------------------ Attractions ------------------
DEFAULT_ATTRACTIONS: List[Dict[str, Any]] = [
    # Northern Region
    {"id":"A001","name":"Murchison Falls National Park","region":"Northern","category":"Wildlife","city":"Nwoya / Masindi","description":"Spectacular falls, wildlife safaris, Nile River views.","opening_hours":"06:00-18:00","entry_fee_usd":40,"popularity":9.5,"image":"murchison.jpg"},
    {"id":"A002","name":"Kidepo Valley National Park","region":"Northern","category":"Wildlife","city":"Kidepo","description":"Remote park with lions, elephants, and buffaloes.","opening_hours":"06:00-17:00","entry_fee_usd":50,"popularity":9.2,"image":"kidepo.jpg"},
    {"id":"A003","name":"Ziwa Rhino Sanctuary","region":"Northern","category":"Wildlife","city":"Nakasongola","description":"Conservation area for rhinos with guided tours.","opening_hours":"07:00-17:00","entry_fee_usd":30,"popularity":8.7,"image":"ziwa.jpg"},
    {"id":"A004","name":"Lira Cultural Center","region":"Northern","category":"Cultural","city":"Lira","description":"Showcases Acholi culture and arts.","opening_hours":"08:00-18:00","entry_fee_usd":5,"popularity":7.8,"image":"lira.jpg"},

    # Western Region
    {"id":"A005","name":"Rwenzori Mountains National Park","region":"Western","category":"Hiking","city":"Kasese","description":"Snow-capped mountains and breathtaking hikes.","opening_hours":"06:00-18:00","entry_fee_usd":35,"popularity":9.3,"image":"rwenzori.jpg"},
    {"id":"A006","name":"Fort Portal Crater Lakes","region":"Western","category":"Natural Wonders","city":"Fort Portal","description":"Beautiful crater lakes surrounded by forest.","opening_hours":"08:00-17:00","entry_fee_usd":5,"popularity":7.5,"image":"crater_lakes.jpg"},
    {"id":"A007","name":"Semuliki National Park","region":"Western","category":"Wildlife","city":"Bundibugyo","description":"Hot springs, wildlife, and lush forest trails.","opening_hours":"06:00-17:00","entry_fee_usd":35,"popularity":8.2,"image":"semuliki.jpg"},
    {"id":"A008","name":"Toro Palace","region":"Western","category":"Cultural","city":"Fort Portal","description":"Traditional palace of the Toro Kingdom.","opening_hours":"09:00-17:00","entry_fee_usd":3,"popularity":6.8,"image":"toro_palace.jpg"},

    # Central Region
    {"id":"A009","name":"Kampala National Mosque","region":"Central","category":"Cultural","city":"Kampala","description":"Panoramic city views from the minaret.","opening_hours":"09:00-17:00","entry_fee_usd":0,"popularity":7.2,"image":"mosque.jpg"},
    {"id":"A010","name":"Ssese Islands","region":"Central","category":"Beaches","city":"Kalangala","description":"Relaxed lakeside beaches and island hopping.","opening_hours":"All day","entry_fee_usd":0,"popularity":7.9,"image":"ssese.jpg"},
    {"id":"A011","name":"Uganda Museum","region":"Central","category":"Cultural","city":"Kampala","description":"Uganda's oldest museum, exhibits history and culture.","opening_hours":"09:00-17:00","entry_fee_usd":3,"popularity":6.8,"image":"museum.jpg"},
    {"id":"A012","name":"Entebbe Botanical Gardens","region":"Central","category":"Natural Wonders","city":"Entebbe","description":"Lush gardens by Lake Victoria.","opening_hours":"07:00-17:00","entry_fee_usd":2,"popularity":7.5,"image":"botanical.jpg"},
    {"id":"A013","name":"Lake Victoria Beaches","region":"Central","category":"Beaches","city":"Entebbe","description":"Sandy beaches and water activities.","opening_hours":"All day","entry_fee_usd":0,"popularity":7.3,"image":"victoria_beach.jpg"},

    # South Western Region
    {"id":"A014","name":"Bwindi Impenetrable Forest","region":"South Western","category":"Wildlife","city":"Kisoro","description":"Home to mountain gorillas and rich biodiversity.","opening_hours":"06:00-17:00","entry_fee_usd":50,"popularity":9.8,"image":"bwindi.jpg"},
    {"id":"A015","name":"Lake Bunyonyi","region":"South Western","category":"Beaches","city":"Kabale","description":"Scenic lake with islands and birdwatching opportunities.","opening_hours":"All day","entry_fee_usd":0,"popularity":8.5,"image":"bunyonyi.jpg"},
    {"id":"A016","name":"Mgahinga Gorilla National Park","region":"South Western","category":"Wildlife","city":"Mgahinga","description":"Gorilla trekking and golden monkeys.","opening_hours":"06:00-17:00","entry_fee_usd":45,"popularity":9.1,"image":"mgahinga.jpg"},
    {"id":"A017","name":"Ishasha Sector","region":"South Western","category":"Wildlife","city":"Queen Elizabeth NP","description":"Tree-climbing lions and safari drives.","opening_hours":"06:00-18:00","entry_fee_usd":40,"popularity":8.9,"image":"ishasha.jpg"},
    {"id":"A018","name":"Queen Elizabeth National Park","region":"South Western","category":"Wildlife","city":"Kasese","description":"Safari park with elephants, lions, and hippos.","opening_hours":"06:00-18:00","entry_fee_usd":40,"popularity":9.4,"image":"queen_elizabeth.jpg"},

    # Additional popular sites (mix)
    {"id":"A019","name":"Zanzibar Market Uganda","region":"Central","category":"Cultural","city":"Kampala","description":"Local crafts, souvenirs, and street food.","opening_hours":"08:00-18:00","entry_fee_usd":0,"popularity":7.0,"image":"zanzibar_market.jpg"},
    {"id":"A020","name":"Sipi Falls","region":"Eastern","category":"Natural Wonders","city":"Kapchorwa","description":"Series of stunning waterfalls and hiking trails.","opening_hours":"06:00-18:00","entry_fee_usd":5,"popularity":8.6,"image":"sipi.jpg"},
    {"id":"A021","name":"Mount Elgon National Park","region":"Eastern","category":"Hiking","city":"Mbale","description":"Volcano hiking and caves exploration.","opening_hours":"06:00-18:00","entry_fee_usd":10,"popularity":8.9,"image":"elgon.jpg"},
    {"id":"A022","name":"Jinja Source of Nile","region":"Eastern","category":"Natural Wonders","city":"Jinja","description":"Where the Nile begins, ideal for rafting and boat rides.","opening_hours":"06:00-18:00","entry_fee_usd":15,"popularity":9.0,"image":"nile.jpg"},
    {"id":"A023","name":"Bujagali Falls","region":"Eastern","category":"Natural Wonders","city":"Jinja","description":"Beautiful falls, popular for water sports.","opening_hours":"06:00-18:00","entry_fee_usd":10,"popularity":8.7,"image":"bujagali.jpg"},
    {"id":"A024","name":"Mbarara Cultural Center","region":"Western","category":"Cultural","city":"Mbarara","description":"Learn Ankole culture and history.","opening_hours":"08:00-17:00","entry_fee_usd":5,"popularity":7.6,"image":"mbarara.jpg"},
    {"id":"A025","name":"Kampala City Walks","region":"Central","category":"Cultural","city":"Kampala","description":"Guided walking tours of the city.","opening_hours":"08:00-18:00","entry_fee_usd":2,"popularity":7.5,"image":"city_walk.jpg"},
    {"id":"A026","name":"Buganda Kingdom Palace","region":"Central","category":"Cultural","city":"Mengo","description":"Royal palace of Buganda Kingdom.","opening_hours":"09:00-17:00","entry_fee_usd":5,"popularity":7.9,"image":"buganda_palace.jpg"},
    {"id":"A027","name":"Mabamba Swamp","region":"Central","category":"Natural Wonders","city":"Entebbe","description":"Birdwatching, especially for the shoebill stork.","opening_hours":"06:00-17:00","entry_fee_usd":5,"popularity":8.3,"image":"mabamba.jpg"},
    {"id":"A028","name":"Lake Mburo National Park","region":"Western","category":"Wildlife","city":"Mbarara","description":"Safari park with zebras and hippos.","opening_hours":"06:00-18:00","entry_fee_usd":35,"popularity":8.5,"image":"mburo.jpg"},
    {"id":"A029","name":"Kampala Night Market","region":"Central","category":"Cultural","city":"Kampala","description":"Nightlife, local food and crafts.","opening_hours":"17:00-23:00","entry_fee_usd":0,"popularity":7.0,"image":"night_market.jpg"},
    {"id":"A030","name":"Kalangala Palm Beaches","region":"Central","category":"Beaches","city":"Kalangala","description":"Relaxing tropical palm beaches.","opening_hours":"All day","entry_fee_usd":0,"popularity":7.8,"image":"kalangala.jpg"},
]


# ------------------ Category Emojis ------------------
CATEGORY_EMOJIS = {
    "Wildlife": "🦁",
    "Hiking": "🗻",
    "Cultural": "🕌",
    "Beaches": "🌊",
    "Natural Wonders": "🌳"
}

# ------------------ Helpers ------------------
def ensure_data_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def save_json(path: Path, obj: Any):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def load_or_init_json(path: Path, default: Any):
    if not path.exists():
        save_json(path, default)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def id_to_num(aid: str) -> int:
    return sum(ord(c) for c in aid)

def generate_default_routes(attractions: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    routes: Dict[str, Dict[str, Any]] = {}
    # CURRENT -> each attraction
    for a in attractions:
        n = id_to_num(a["id"])
        dist = 20 + (n % 400)
        time_min = int(dist * 1.8) + (n % 25)
        routes[f"CURRENT__{a['id']}"] = {
            "distance_km": dist,
            "time_min": time_min,
            "steps": [f"Drive from CURRENT location to {a['name']} in {a['city']}"]
        }
    # attraction -> attraction (directed)
    for a, b in itertools.permutations(attractions, 2):
        n = abs(id_to_num(a["id"]) - id_to_num(b["id"]))
        dist = 8 + (n % 250)
        time_min = int(dist * 2) + (n % 20)
        key = f"{a['id']}{b['id']}"
        routes[key] = {
            "distance_km": dist,
            "time_min": time_min,
            "steps": [f"Drive from {a['city']} to {b['city']} (main road)", f"Arrive at {b['name']}"]
        }
    return routes

def find_attraction(attractions: List[Dict[str, Any]], aid: str) -> Dict[str, Any]:
    aid = (aid or "").strip().upper()
    for a in attractions:
        if a["id"].upper() == aid:
            return a
    return None

def display_attractions_list(attractions: List[Dict[str, Any]]):
    print()
    for a in attractions:
        emoji = CATEGORY_EMOJIS.get(a["category"], "📍")
        print(f"{a['id']}: {emoji} {a['name']} — {a['city']} (Pop {a['popularity']})")
    print()

def open_image_file(filename: str):
    path = IMAGES_DIR / filename
    if not path.exists():
        print(f"⚠ Image not found: {path}  — put the file in data/images/")
        return
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":
            subprocess.run(["open", str(path)])
        else:
            # Linux and other: try xdg-open
            subprocess.run(["xdg-open", str(path)])
    except Exception as e:
        print("⚠ Could not open image automatically (", e, "). Path:", path)

def open_google_maps(origin: str, destination: str):
    o = origin or ""
    d = destination or ""
    url = f"https://www.google.com/maps/dir/?api=1&origin={quote_plus(o)}&destination={quote_plus(d)}"
    try:
        webbrowser.open(url)
    except Exception as e:
        print("⚠ Could not open browser:", e)
    return url

def get_route(routes: Dict[str, Any], from_id: str, to_id: str) -> Dict[str, Any]:
    key = f"{from_id.upper()}{to_id.upper()}"
    if key in routes:
        return routes[key]
    # fallback dynamic
    a_num = id_to_num(from_id)
    b_num = id_to_num(to_id)
    n = abs(a_num - b_num)
    dist = 10 + (n % 300)
    time_min = int(dist * 2) + (n % 20)
    return {"distance_km": dist, "time_min": time_min, "steps":[f"Drive from {from_id} to {to_id}"]}

def display_route(route: Dict[str, Any]):
    print(f"\nDistance: {route['distance_km']} km | Time: {route['time_min']} minutes")
    for i, step in enumerate(route.get("steps", []), start=1):
        print(f"{i}. {step}")
    print()
