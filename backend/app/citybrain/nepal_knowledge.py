"""Curated Nepal intelligence used by CityBrain to ground its reasoning."""
from typing import Dict, List, Any

CITIES: Dict[str, Dict[str, Any]] = {
    "Kathmandu": {"lat": 27.7172, "lon": 85.3240, "region": "Bagmati",
                   "desc": "Capital; temples, Thamel, Durbar Square, Boudha & Pashupatinath."},
    "Lalitpur": {"lat": 27.6588, "lon": 85.3247, "region": "Bagmati",
                  "desc": "Patan; Newari arts, Patan Durbar Square, Golden Temple."},
    "Bhaktapur": {"lat": 27.6710, "lon": 85.4298, "region": "Bagmati",
                   "desc": "Medieval city; pottery, juju dhau, Nyatapola temple."},
    "Pokhara": {"lat": 28.2096, "lon": 83.9856, "region": "Gandaki",
                 "desc": "Lakeside gateway to Annapurna; paragliding, Phewa Lake."},
    "Chitwan": {"lat": 27.5291, "lon": 84.3542, "region": "Bagmati",
                 "desc": "Chitwan National Park; jungle safari, rhinos, tigers."},
    "Lumbini": {"lat": 27.4833, "lon": 83.2767, "region": "Lumbini",
                 "desc": "Birthplace of Buddha; monastic zone, Maya Devi Temple."},
    "Dharan": {"lat": 26.8147, "lon": 87.2769, "region": "Koshi",
                "desc": "Eastern hill town; Dantakali, Budha Subba."},
    "Janakpur": {"lat": 26.7271, "lon": 85.9407, "region": "Madhesh",
                  "desc": "Janaki Mandir; Mithila culture, Ram-Sita heritage."},
    "Biratnagar": {"lat": 26.4525, "lon": 87.2718, "region": "Koshi",
                    "desc": "Industrial hub in the eastern Terai."},
    "Butwal": {"lat": 27.7006, "lon": 83.4484, "region": "Lumbini",
                "desc": "Gateway between hills and Terai; Siddhababa temple."},
    "Ilam": {"lat": 26.9094, "lon": 87.9286, "region": "Koshi",
              "desc": "Tea gardens, rolling hills, Mai Pokhari, Kanyam."},
    "Mustang": {"lat": 28.7800, "lon": 83.7190, "region": "Gandaki",
                 "desc": "Jomsom/Upper Mustang; Trans-Himalaya, Muktinath."},
}

EMERGENCY_NUMBERS: List[Dict[str, str]] = [
    {"name": "Police", "number": "100", "icon": "shield"},
    {"name": "Ambulance", "number": "102", "icon": "ambulance"},
    {"name": "Fire Brigade", "number": "101", "icon": "flame"},
    {"name": "Tourist Police", "number": "1144", "icon": "badge"},
    {"name": "Traffic Police", "number": "103", "icon": "car"},
    {"name": "Nepal Red Cross", "number": "01-4228094", "icon": "cross"},
]

FESTIVALS: List[Dict[str, str]] = [
    {"name": "Dashain", "period": "Sep-Oct", "month": "Ashwin",
     "about": "Nepal's biggest festival; family gatherings, tika, jamara, kite flying. Many shops and transport run reduced for ~2 weeks."},
    {"name": "Tihar (Deepawali)", "period": "Oct-Nov", "month": "Kartik",
     "about": "Festival of lights; Laxmi Puja, Bhai Tika; crows, dogs and cows honored over five days."},
    {"name": "Holi (Fagu Purnima)", "period": "Mar", "month": "Falgun",
     "about": "Festival of colors; celebrated a day earlier in the hills than the Terai."},
    {"name": "Indra Jatra", "period": "Sep", "month": "Bhadra",
     "about": "Kathmandu chariot festival; living goddess Kumari procession, Lakhe masked dances."},
    {"name": "Bisket Jatra", "period": "Apr", "month": "Baisakh",
     "about": "Bhaktapur New Year chariot festival with tongue-piercing and pole-raising rituals."},
    {"name": "Losar", "period": "Feb", "month": "Magh",
     "about": "Tibetan/Sherpa/Tamang/Gurung New Year; vibrant in Boudha and mountain regions."},
]

ETIQUETTE: List[str] = [
    "Greet with 'Namaste' (palms together). Give/receive with the right hand or both hands.",
    "Remove shoes before entering temples and homes. Walk clockwise around stupas and shrines.",
    "Do not touch anyone's head; avoid pointing your feet at people or deities.",
    "Ask before photographing people, sadhus, or temple interiors (some prohibit photos).",
    "Dress modestly at religious sites; cover shoulders and knees.",
    "Non-Hindus may not enter certain temple sanctums (e.g., Pashupatinath main shrine).",
    "Beef is avoided (cows are sacred). Use your right hand when eating with hands.",
]

SAFETY: Dict[str, List[str]] = {
    "monsoon": [
        "Monsoon runs mid-June to September with heavy afternoon rain and leeches on trails.",
        "Landslides and roadblocks are common on hill highways (Prithvi, Mugling-Narayanghat).",
        "Domestic flights are often delayed/cancelled by cloud cover (Pokhara/Jomsom/Lukla).",
        "Carry rain gear, waterproof bags, and add buffer days to your plan.",
    ],
    "landslide": [
        "Avoid hill roads during/after heavy rain; check Nepal Police road updates.",
        "Mugling-Narayanghat and the Prithvi Highway are landslide-prone in monsoon.",
        "Prefer daytime travel; keep emergency contacts and offline maps ready.",
    ],
    "earthquake": [
        "Nepal is in a high seismic zone. During shaking: Drop, Cover, Hold On.",
        "Identify safe spots (under sturdy tables, away from windows) in your accommodation.",
        "Keep a go-bag: water, torch, power bank, document copies, and cash.",
    ],
    "altitude": [
        "Above 2,500m ascend slowly; watch for AMS (headache, nausea, dizziness).",
        "Hydrate, avoid alcohol, and descend if symptoms worsen. Consider Diamox after advice.",
    ],
}

PRACTICAL: Dict[str, Dict[str, str]] = {
    "currency": {"title": "Currency & Money",
        "info": "Nepali Rupee (NPR / Rs); USD ~ Rs 133. Carry cash outside cities; cards work in tourist areas. ATMs charge ~Rs 500 per withdrawal. Indian Rs 500/2000 notes are not accepted."},
    "sim": {"title": "SIM & Connectivity",
        "info": "Ncell and Nepal Telecom (NTC) offer tourist SIMs at the airport and shops with passport + photo. NTC has better mountain coverage; Ncell is fast in cities."},
    "tims": {"title": "Trekking Permits (TIMS)",
        "info": "A TIMS card is required for most treks; arrange via NTB/TAAN in Kathmandu/Pokhara. Conservation area permits (ACAP/national park entry) are separate. Restricted areas (Upper Mustang/Manaslu) need a registered guide."},
    "border": {"title": "Borders & Entry",
        "info": "Main India crossings: Sunauli (Bhairahawa), Birgunj, Kakarbhitta, Nepalgunj. Tibet via Rasuwagadhi/Kerung (special permits required). Visa-on-arrival at Tribhuvan (TIA), bring USD + photos."},
    "etiquette": {"title": "Etiquette & Culture",
        "info": " ".join(ETIQUETTE)},
    "cuisine": {"title": "Food & Cuisine",
        "info": "Must-try: dal bhat (rice, lentils, curry), momo (dumplings), Newari samay baji, sel roti, juju dhau (Bhaktapur curd), thakali set, and Ilam tea."},
}

TREKS: List[Dict[str, str]] = [
    {"name": "Annapurna Base Camp (ABC)", "region": "Gandaki", "days": "7-12",
     "difficulty": "Moderate", "max_alt": "4,130 m", "permits": "TIMS + ACAP"},
    {"name": "Everest Base Camp (EBC)", "region": "Khumbu", "days": "12-14",
     "difficulty": "Challenging", "max_alt": "5,364 m", "permits": "Sagarmatha NP + Khumbu Pasang Lhamu"},
    {"name": "Langtang Valley", "region": "Bagmati", "days": "7-10",
     "difficulty": "Moderate", "max_alt": "4,984 m (Kyanjin Ri)", "permits": "TIMS + Langtang NP"},
    {"name": "Ghorepani Poon Hill", "region": "Gandaki", "days": "4-5",
     "difficulty": "Easy-Moderate", "max_alt": "3,210 m", "permits": "TIMS + ACAP"},
    {"name": "Manaslu Circuit", "region": "Gandaki", "days": "14-18",
     "difficulty": "Challenging", "max_alt": "5,106 m (Larke Pass)", "permits": "Restricted Area + MCAP + guide"},
    {"name": "Mardi Himal", "region": "Gandaki", "days": "4-6",
     "difficulty": "Moderate", "max_alt": "4,500 m", "permits": "TIMS + ACAP"},
]

UNESCO_SITES: List[str] = [
    "Kathmandu Durbar Square", "Patan Durbar Square", "Bhaktapur Durbar Square",
    "Swayambhunath", "Boudhanath", "Pashupatinath", "Changu Narayan",
    "Lumbini (Birthplace of the Buddha)", "Sagarmatha National Park", "Chitwan National Park",
]

TRANSPORT: List[Dict[str, str]] = [
    {"route": "Kathmandu \u2194 Pokhara", "mode": "Tourist Bus", "duration": "6-8 hrs",
     "fare_npr": "800-2000", "notes": "Greenline/Tourist buses from Sorhakhutte/Kantipath; flights ~25 min."},
    {"route": "Kathmandu \u2194 Chitwan (Sauraha)", "mode": "Tourist Bus", "duration": "5-6 hrs",
     "fare_npr": "700-1500", "notes": "Via Mugling; book a day ahead in peak season."},
    {"route": "Kathmandu \u2194 Lumbini", "mode": "Bus / Flight", "duration": "8-9 hrs bus",
     "fare_npr": "1000-1800", "notes": "Fly to Bhairahawa (Gautam Buddha Airport) then 30 min drive."},
    {"route": "Pokhara \u2194 Jomsom", "mode": "Flight / Jeep", "duration": "20 min flight",
     "fare_npr": "", "notes": "Gateway to Muktinath & Upper Mustang; weather-dependent flights."},
    {"route": "Within cities", "mode": "Taxi / Pathao / InDrive", "duration": "-",
     "fare_npr": "150-700", "notes": "Use ride-hailing apps to avoid haggling; micro-buses are cheapest."},
]


def knowledge_brief() -> str:
    fest = "; ".join(f"{f['name']} ({f['period']})" for f in FESTIVALS)
    return (
        "NEPAL CONTEXT: Currency=NPR (Rs). "
        f"Major festivals: {fest}. "
        "Etiquette: say Namaste, remove shoes at temples, walk clockwise around stupas, "
        "dress modestly, ask before photos, beef avoided. "
        "Emergency: Police 100, Ambulance 102, Fire 101, Tourist Police 1144."
    )
