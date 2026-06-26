"""Nepal-specific knowledge base for CityBrain (POC subset).

This is the curated, real-world Nepal intelligence the agents reason over.
The full app expands this into MongoDB collections; here we keep an
in-memory subset to prove the orchestration + reasoning works.
"""
from typing import Dict, List, Any

# --- Cities with real coordinates (lat, lon) ---
CITIES: Dict[str, Dict[str, Any]] = {
    "Kathmandu": {"lat": 27.7172, "lon": 85.3240, "region": "Bagmati",
                   "desc": "Capital city; temples, Thamel nightlife, Durbar Square."},
    "Lalitpur": {"lat": 27.6588, "lon": 85.3247, "region": "Bagmati",
                  "desc": "Patan; fine Newari arts, Patan Durbar Square."},
    "Bhaktapur": {"lat": 27.6710, "lon": 85.4298, "region": "Bagmati",
                   "desc": "Medieval city; pottery, juju dhau, Nyatapola temple."},
    "Pokhara": {"lat": 28.2096, "lon": 83.9856, "region": "Gandaki",
                 "desc": "Lakeside gateway to Annapurna; paragliding, Phewa Lake."},
    "Chitwan": {"lat": 27.5291, "lon": 84.3542, "region": "Bagmati",
                 "desc": "Chitwan National Park; jungle safari, rhinos, tigers."},
    "Lumbini": {"lat": 27.4833, "lon": 83.2767, "region": "Lumbini",
                 "desc": "Birthplace of Buddha; monastic zone, Maya Devi Temple."},
    "Dharan": {"lat": 26.8147, "lon": 87.2769, "region": "Koshi",
                "desc": "Eastern hill town; Dantakali, BP Koirala Institute."},
    "Janakpur": {"lat": 26.7271, "lon": 85.9407, "region": "Madhesh",
                  "desc": "Janaki Mandir; Mithila culture, Ram-Sita heritage."},
    "Biratnagar": {"lat": 26.4525, "lon": 87.2718, "region": "Koshi",
                    "desc": "Industrial hub in the eastern Terai."},
    "Butwal": {"lat": 27.7006, "lon": 83.4484, "region": "Lumbini",
                "desc": "Gateway between hills and Terai on the Siddhartha Highway."},
    "Ilam": {"lat": 26.9094, "lon": 87.9286, "region": "Koshi",
              "desc": "Tea gardens, rolling green hills, Mai Pokhari."},
    "Mustang": {"lat": 28.7800, "lon": 83.7190, "region": "Gandaki",
                 "desc": "Jomsom/Upper Mustang; Trans-Himalayan desert, Muktinath."},
}

# --- Emergency numbers (national) ---
EMERGENCY_NUMBERS: List[Dict[str, str]] = [
    {"name": "Police", "number": "100"},
    {"name": "Ambulance", "number": "102"},
    {"name": "Fire Brigade", "number": "101"},
    {"name": "Tourist Police", "number": "1144"},
    {"name": "Traffic Police", "number": "103"},
    {"name": "Nepal Red Cross Ambulance", "number": "4228094"},
]

# --- Festivals ---
FESTIVALS: List[Dict[str, str]] = [
    {"name": "Dashain", "period": "Sep-Oct", "about": "Nepal's biggest festival; family gatherings, tika, kite flying. Many shops/transport reduced for ~2 weeks."},
    {"name": "Tihar", "period": "Oct-Nov", "about": "Festival of lights; Laxmi Puja, Bhai Tika, dogs/crows honored."},
    {"name": "Holi", "period": "Mar", "about": "Festival of colors; played a day earlier in the hills than the Terai."},
    {"name": "Indra Jatra", "period": "Sep", "about": "Kathmandu chariot festival; Kumari procession, masked dances."},
    {"name": "Losar", "period": "Feb", "about": "Tibetan/Sherpa/Tamang New Year; vibrant in Boudha & mountain regions."},
]

# --- Etiquette & culture tips ---
ETIQUETTE: List[str] = [
    "Greet with 'Namaste' (palms together). Use the right hand or both hands to give/receive.",
    "Remove shoes before entering temples and homes. Walk clockwise around stupas and shrines.",
    "Do not touch anyone's head; avoid pointing feet at people or deities.",
    "Ask before photographing people, sadhus, or inside temples (some prohibit photos).",
    "Dress modestly at religious sites; cover shoulders and knees.",
    "Non-Hindus may not be allowed inside certain temple sanctums (e.g., Pashupatinath main shrine).",
    "Beef is avoided (cow is sacred); many Hindus are vegetarian on certain days.",
]

# --- Safety / hazard guidance ---
SAFETY: Dict[str, List[str]] = {
    "monsoon": [
        "Monsoon runs mid-June to September; expect heavy afternoon rain and leeches on trails.",
        "Landslides and road blocks are common on hill highways (Prithvi, Mugling, Narayanghat).",
        "Domestic flights are frequently delayed/cancelled by cloud cover, esp. Pokhara/Jomsom/Lukla.",
        "Carry rain gear, waterproof bags, and buffer days into your itinerary.",
    ],
    "landslide": [
        "Avoid travelling on hill roads during/after heavy rain; check Nepal Police road updates.",
        "Mugling-Narayanghat and Prithvi Highway are landslide-prone in monsoon.",
        "Prefer daytime travel; keep emergency contacts and offline maps handy.",
    ],
    "earthquake": [
        "Nepal is in a high seismic zone. Drop, Cover, Hold On during shaking.",
        "Identify safe spots (under sturdy tables, away from windows) in your accommodation.",
        "Keep a small go-bag: water, torch, power bank, copies of documents, cash.",
    ],
    "altitude": [
        "Above 2,500m, ascend slowly; watch for AMS (headache, nausea, dizziness).",
        "Hydrate, avoid alcohol, and descend if symptoms worsen. Consider Diamox after advice.",
    ],
}

# --- Practical traveler info ---
PRACTICAL: Dict[str, str] = {
    "currency": "Nepali Rupee (NPR / Rs). USD ~ Rs 133. Carry cash outside cities; cards accepted in tourist areas. ATMs charge ~Rs 500/withdrawal.",
    "sim": "Ncell and Nepal Telecom (NTC) offer tourist SIMs at the airport/shops with passport + photo. NTC has better mountain coverage.",
    "tims": "TIMS (Trekkers' Information Management System) card is required for most treks; arrange via NTB/TAAN in Kathmandu/Pokhara. Conservation area permits (ACAP/national park) are separate.",
    "border": "Main India borders: Sunauli (Bhairahawa), Birgunj, Kakarbhitta, Nepalgunj. Tibet via Rasuwagadhi/Kerung (permits required).",
}

# --- Curated sample places (POC subset of real, well-known places) ---
SAMPLE_PLACES: List[Dict[str, Any]] = [
    # Pokhara
    {"name": "Phewa Lake", "city": "Pokhara", "type": "attraction", "lat": 28.2096, "lon": 83.9485, "price_npr": 0, "about": "Iconic lake with boating to Tal Barahi temple; sunset views of Annapurna."},
    {"name": "World Peace Pagoda", "city": "Pokhara", "type": "attraction", "lat": 28.1958, "lon": 83.9456, "price_npr": 0, "about": "Hilltop stupa with panoramic lake and mountain views; short hike or boat+walk."},
    {"name": "Sarangkot", "city": "Pokhara", "type": "attraction", "lat": 28.2440, "lon": 83.9490, "price_npr": 0, "about": "Famous sunrise viewpoint over the Annapurnas; paragliding launch site."},
    {"name": "Or2k Pokhara", "city": "Pokhara", "type": "restaurant", "lat": 28.2138, "lon": 83.9588, "price_npr": 600, "about": "Popular vegetarian/Middle-Eastern cafe in Lakeside; budget-friendly."},
    {"name": "Hotel Lakeside", "city": "Pokhara", "type": "hotel", "lat": 28.2110, "lon": 83.9570, "price_npr": 2500, "about": "Mid-range lakeside hotel walking distance to restaurants."},
    # Kathmandu
    {"name": "Boudhanath Stupa", "city": "Kathmandu", "type": "attraction", "lat": 27.7215, "lon": 85.3620, "price_npr": 400, "about": "One of the world's largest stupas; Tibetan Buddhist hub, kora walk at dusk."},
    {"name": "Pashupatinath Temple", "city": "Kathmandu", "type": "attraction", "lat": 27.7104, "lon": 85.3488, "price_npr": 1000, "about": "Sacred Hindu temple on the Bagmati; cremation ghats, evening aarti."},
    {"name": "Kathmandu Durbar Square", "city": "Kathmandu", "type": "attraction", "lat": 27.7044, "lon": 85.3070, "price_npr": 1000, "about": "Historic royal palace square; Kumari Ghar, Newari architecture."},
    {"name": "Thamel", "city": "Kathmandu", "type": "attraction", "lat": 27.7151, "lon": 85.3110, "price_npr": 0, "about": "Backpacker hub; shops, trekking gear, cafes, nightlife."},
    {"name": "OR2K Thamel", "city": "Kathmandu", "type": "restaurant", "lat": 27.7148, "lon": 85.3115, "price_npr": 700, "about": "Lively vegetarian restaurant with floor seating in Thamel."},
]


def nearest_city(lat: float, lon: float) -> str:
    best, best_d = "Kathmandu", 1e9
    for name, c in CITIES.items():
        d = (c["lat"] - lat) ** 2 + (c["lon"] - lon) ** 2
        if d < best_d:
            best, best_d = name, d
    return best


def places_in_city(city: str, ptype: str = None) -> List[Dict[str, Any]]:
    out = [p for p in SAMPLE_PLACES if p["city"].lower() == (city or "").lower()]
    if ptype:
        out = [p for p in out if p["type"] == ptype]
    return out


def knowledge_brief() -> str:
    """A compact Nepal context block to ground the merger LLM."""
    fest = "; ".join(f"{f['name']} ({f['period']})" for f in FESTIVALS)
    return (
        "NEPAL CONTEXT: Currency=NPR. "
        f"Major festivals: {fest}. "
        "Etiquette: say Namaste, remove shoes at temples, walk clockwise around stupas, "
        "dress modestly, ask before photos. Emergency: Police 100, Ambulance 102, "
        "Fire 101, Tourist Police 1144."
    )
