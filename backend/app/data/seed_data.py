"""Curated, real Nepal places dataset (Phase 2 seed).

Names, locations, coordinates and descriptions are real. Photos are
representative stock images (verified-stable Pexels CDN URLs) assigned by
category for a consistent premium look.
"""
from typing import Dict, List, Any

# Verified-stable Pexels CDN images, grouped by vibe.
_IMG = {
    "mountain": [
        "https://images.pexels.com/photos/9275921/pexels-photo-9275921.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "https://images.pexels.com/photos/25490311/pexels-photo-25490311.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "https://images.pexels.com/photos/25490313/pexels-photo-25490313.jpeg?auto=compress&cs=tinysrgb&w=1200",
    ],
    "heritage": [
        "https://images.pexels.com/photos/19279803/pexels-photo-19279803.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "https://images.pexels.com/photos/14555236/pexels-photo-14555236.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "https://images.pexels.com/photos/2440021/pexels-photo-2440021.jpeg?auto=compress&cs=tinysrgb&w=1200",
    ],
    "restaurant": [
        "https://images.pexels.com/photos/1058277/pexels-photo-1058277.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg?auto=compress&cs=tinysrgb&w=1200",
    ],
    "hotel": [
        "https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "https://images.pexels.com/photos/2474690/pexels-photo-2474690.jpeg?auto=compress&cs=tinysrgb&w=1200",
    ],
    "event": [
        "https://images.pexels.com/photos/3389528/pexels-photo-3389528.jpeg?auto=compress&cs=tinysrgb&w=1200",
    ],
}


def _img(category: str, idx: int) -> str:
    pool = _IMG.get(category, _IMG["heritage"])
    return pool[idx % len(pool)]


# (name, type, city, region, lat, lon, price_npr, rating, tags, hours, description)
_RAW: List[tuple] = [
    # ---------------- KATHMANDU ----------------
    ("Boudhanath Stupa", "attraction", "Kathmandu", "Bagmati", 27.7215, 85.3620, 400, 4.8,
     ["unesco", "buddhist", "spiritual"], "Daily 4:00 AM - 9:00 PM",
     "One of the world's largest spherical stupas and a hub of Tibetan Buddhism. Join the evening kora (clockwise walk) as butter lamps glow."),
    ("Pashupatinath Temple", "attraction", "Kathmandu", "Bagmati", 27.7104, 85.3488, 1000, 4.7,
     ["unesco", "hindu", "spiritual"], "Daily 4:00 AM - 9:00 PM",
     "Nepal's holiest Hindu temple on the Bagmati River, famous for its cremation ghats and the spectacular evening Bagmati Aarti."),
    ("Swayambhunath (Monkey Temple)", "attraction", "Kathmandu", "Bagmati", 27.7149, 85.2904, 200, 4.7,
     ["unesco", "buddhist", "viewpoint"], "Daily 24 hrs",
     "Hilltop stupa with the all-seeing Buddha eyes and sweeping views over the Kathmandu Valley. Climb the 365 stone steps among playful monkeys."),
    ("Kathmandu Durbar Square", "attraction", "Kathmandu", "Bagmati", 27.7044, 85.3070, 1000, 4.6,
     ["unesco", "heritage", "history"], "Daily 9:00 AM - 6:00 PM",
     "Historic royal plaza of palaces, courtyards and temples, including the Kumari Ghar, home of Nepal's living goddess."),
    ("Garden of Dreams", "attraction", "Kathmandu", "Bagmati", 27.7137, 85.3157, 400, 4.5,
     ["garden", "relax", "cafe"], "Daily 9:00 AM - 10:00 PM",
     "A serene neo-classical garden oasis beside Thamel, perfect for a quiet break with a coffee away from the city buzz."),
    ("Thamel", "attraction", "Kathmandu", "Bagmati", 27.7151, 85.3110, 0, 4.4,
     ["nightlife", "shopping", "backpacker"], "Open all day",
     "Kathmandu's vibrant tourist heart packed with trekking gear shops, cafes, live-music bars and souvenir stalls."),
    ("Hotel Yak & Yeti", "hotel", "Kathmandu", "Bagmati", 27.7106, 85.3220, 12000, 4.6,
     ["luxury", "heritage", "pool"], "Check-in 2:00 PM",
     "Iconic 5-star heritage hotel built around a former Rana palace, with gardens, a pool and renowned dining."),
    ("Kathmandu Guest House", "hotel", "Kathmandu", "Bagmati", 27.7155, 85.3107, 4500, 4.5,
     ["heritage", "garden", "central"], "Check-in 1:00 PM",
     "The legendary Thamel institution with a leafy courtyard; the original base camp of Himalayan expeditions."),
    ("Aloft Kathmandu Thamel", "hotel", "Kathmandu", "Bagmati", 27.7146, 85.3119, 9000, 4.5,
     ["modern", "rooftop", "central"], "Check-in 3:00 PM",
     "Contemporary hotel in the middle of Thamel with a rooftop bar and easy access to nightlife and shopping."),
    ("Hotel Backpackers", "hotel", "Kathmandu", "Bagmati", 27.7160, 85.3120, 1500, 4.1,
     ["budget", "central", "hostel"], "Check-in 12:00 PM",
     "Clean, friendly budget rooms in Thamel — a solid value base for exploring on a shoestring."),
    ("OR2K", "restaurant", "Kathmandu", "Bagmati", 27.7148, 85.3115, 700, 4.6,
     ["vegetarian", "middle-eastern", "lively"], "Daily 9:00 AM - 11:00 PM",
     "Beloved cushion-seating vegetarian restaurant in Thamel with mezze platters, falafel and a buzzing vibe."),
    ("Bhojan Griha", "restaurant", "Kathmandu", "Bagmati", 27.7058, 85.3258, 1800, 4.5,
     ["newari", "nepali", "cultural"], "Daily 11:00 AM - 10:00 PM",
     "Traditional Nepali fine dining in a restored 150-year-old mansion, with a cultural dance show and a Newari thali."),
    ("Yangling Tibetan Restaurant", "restaurant", "Kathmandu", "Bagmati", 27.7156, 85.3110, 450, 4.4,
     ["tibetan", "momo", "budget"], "Daily 8:00 AM - 9:30 PM",
     "Famous for steaming plates of buff and veg momos and thukpa at honest prices, right in Thamel."),
    ("Roadhouse Cafe", "restaurant", "Kathmandu", "Bagmati", 27.7147, 85.3112, 900, 4.4,
     ["pizza", "wood-fired", "cozy"], "Daily 11:00 AM - 10:00 PM",
     "Wood-fired pizzas and a warm fireplace courtyard — a reliable Thamel comfort spot."),

    # ---------------- LALITPUR (PATAN) ----------------
    ("Patan Durbar Square", "attraction", "Lalitpur", "Bagmati", 27.6726, 85.3253, 1000, 4.8,
     ["unesco", "newari", "art"], "Daily 7:00 AM - 7:00 PM",
     "The finest ensemble of Newari architecture in Nepal — intricately carved temples, the Krishna Mandir and the Patan Museum."),
    ("Patan Museum", "attraction", "Lalitpur", "Bagmati", 27.6735, 85.3255, 1000, 4.7,
     ["museum", "art", "history"], "Daily 10:30 AM - 5:30 PM",
     "One of South Asia's best museums of sacred art, set inside a beautifully restored palace courtyard."),
    ("Golden Temple (Hiranya Varna Mahavihar)", "attraction", "Lalitpur", "Bagmati", 27.6749, 85.3242, 100, 4.6,
     ["buddhist", "heritage"], "Daily 9:00 AM - 6:00 PM",
     "A gilded 12th-century Buddhist monastery glittering with metalwork, tucked in the lanes of Patan."),
    ("The Old House", "restaurant", "Lalitpur", "Bagmati", 27.6760, 85.3250, 1600, 4.5,
     ["french", "fine-dining", "courtyard"], "Daily 11:00 AM - 10:00 PM",
     "Elegant French-Nepali dining in a heritage courtyard near Patan Durbar Square."),
    ("Hotel Himalaya", "hotel", "Lalitpur", "Bagmati", 27.6700, 85.3140, 8000, 4.4,
     ["pool", "mountain-view", "business"], "Check-in 2:00 PM",
     "Long-standing comfortable hotel with a pool and Himalayan views on clear mornings."),

    # ---------------- BHAKTAPUR ----------------
    ("Bhaktapur Durbar Square", "attraction", "Bhaktapur", "Bagmati", 27.6722, 85.4280, 1800, 4.8,
     ["unesco", "heritage", "newari"], "Daily 24 hrs (entry desk 7-7)",
     "A living medieval city of brick and timber, with the 55-Window Palace, Nyatapola Temple and Pottery Square."),
    ("Nyatapola Temple", "attraction", "Bhaktapur", "Bagmati", 27.6712, 85.4298, 0, 4.7,
     ["heritage", "temple"], "Daily 24 hrs",
     "Nepal's tallest pagoda (five tiers), guarded by stone wrestlers, elephants and lions on its grand stairway."),
    ("Pottery Square", "attraction", "Bhaktapur", "Bagmati", 27.6700, 85.4270, 0, 4.5,
     ["craft", "culture", "photography"], "Daily morning - evening",
     "Watch potters shape clay on traditional wheels and rows of pots drying in the sun — a centuries-old craft."),
    ("Juju Dhau & King Curd House", "restaurant", "Bhaktapur", "Bagmati", 27.6718, 85.4285, 300, 4.6,
     ["dessert", "local", "famous"], "Daily 8:00 AM - 8:00 PM",
     "Home of 'juju dhau' (the King of Curds) — thick, sweet buffalo-milk yogurt served in clay bowls."),

    # ---------------- POKHARA ----------------
    ("Phewa Lake", "attraction", "Pokhara", "Gandaki", 28.2096, 83.9485, 0, 4.8,
     ["lake", "boating", "sunset"], "Open all day",
     "Pokhara's serene centerpiece; row to the Tal Barahi temple island and watch the Annapurnas mirror on the water at dusk."),
    ("World Peace Pagoda", "attraction", "Pokhara", "Gandaki", 28.1958, 83.9456, 0, 4.7,
     ["viewpoint", "buddhist", "hike"], "Daily 6:00 AM - 6:00 PM",
     "A gleaming white hilltop stupa with panoramic views of Phewa Lake and the Himalaya; reach it by boat-plus-hike."),
    ("Sarangkot", "attraction", "Pokhara", "Gandaki", 28.2440, 83.9490, 0, 4.7,
     ["sunrise", "viewpoint", "paragliding"], "Best at sunrise",
     "The classic sunrise viewpoint over Annapurna and Machhapuchhre, and the launch site for paragliding flights."),
    ("Davis Falls", "attraction", "Pokhara", "Gandaki", 28.1869, 83.9580, 50, 4.2,
     ["waterfall", "nature"], "Daily 6:00 AM - 6:00 PM",
     "A dramatic waterfall that vanishes into an underground tunnel, paired with the Gupteshwor Cave across the road."),
    ("International Mountain Museum", "attraction", "Pokhara", "Gandaki", 28.1909, 83.9743, 600, 4.4,
     ["museum", "mountaineering"], "Daily 9:00 AM - 5:00 PM",
     "Engaging exhibits on Himalayan peaks, mountaineering history and the cultures of Nepal's mountain peoples."),
    ("Begnas Lake", "attraction", "Pokhara", "Gandaki", 28.1700, 84.0900, 0, 4.5,
     ["lake", "quiet", "nature"], "Open all day",
     "A tranquil, less-touristy lake east of Pokhara — great for boating, swimming and lakeside cafes."),
    ("Temple Tree Resort & Spa", "hotel", "Pokhara", "Gandaki", 28.2117, 83.9573, 9500, 4.6,
     ["lakeside", "spa", "pool"], "Check-in 2:00 PM",
     "Stylish lakeside resort with a pool and spa, steps from the Lakeside strip."),
    ("Hotel Lake Star", "hotel", "Pokhara", "Gandaki", 28.2110, 83.9570, 2500, 4.3,
     ["lakeside", "value", "rooftop"], "Check-in 12:00 PM",
     "Comfortable mid-range lakeside hotel with a rooftop view and easy access to restaurants."),
    ("Hotel Travel Inn", "hotel", "Pokhara", "Gandaki", 28.2125, 83.9585, 1400, 4.2,
     ["budget", "central", "garden"], "Check-in 12:00 PM",
     "Friendly budget hotel with a garden in the heart of Lakeside."),
    ("Caffe Concerto", "restaurant", "Pokhara", "Gandaki", 28.2130, 83.9580, 850, 4.5,
     ["italian", "lakeside", "pizza"], "Daily 11:00 AM - 10:00 PM",
     "Authentic wood-fired Italian pizzas and pasta on the Lakeside, run by an Italian chef."),
    ("Or2k Pokhara", "restaurant", "Pokhara", "Gandaki", 28.2138, 83.9588, 650, 4.5,
     ["vegetarian", "lively", "budget"], "Daily 9:00 AM - 11:00 PM",
     "The lakeside sibling of the Thamel favorite — mezze, falafel and fresh juices with cushion seating."),
    ("Godfather's Pizzeria", "restaurant", "Pokhara", "Gandaki", 28.2120, 83.9575, 750, 4.4,
     ["pizza", "casual", "lakeside"], "Daily 11:00 AM - 10:30 PM",
     "A long-time Lakeside favorite for generous, crispy thin-crust pizzas."),

    # ---------------- CHITWAN ----------------
    ("Chitwan National Park", "attraction", "Chitwan", "Bagmati", 27.5291, 84.3542, 2000, 4.8,
     ["unesco", "wildlife", "safari"], "Daily 6:00 AM - 6:00 PM",
     "Nepal's first national park and a UNESCO site, home to one-horned rhinos, Bengal tigers, gharials and 500+ bird species."),
    ("Elephant Breeding Center", "attraction", "Chitwan", "Bagmati", 27.5797, 84.4810, 200, 4.3,
     ["wildlife", "family"], "Daily 6:00 AM - 5:00 PM",
     "See elephant calves and learn about conservation at this center near Sauraha."),
    ("Sauraha Riverside", "attraction", "Chitwan", "Bagmati", 27.5800, 84.4900, 0, 4.4,
     ["sunset", "river", "relax"], "Open all day",
     "The gateway hub to Chitwan, with Rapti River sunset views, canoe trips and Tharu cultural shows."),
    ("Barahi Jungle Lodge", "hotel", "Chitwan", "Bagmati", 27.5680, 84.4960, 14000, 4.7,
     ["luxury", "riverside", "safari"], "Check-in 2:00 PM",
     "Premium riverside jungle lodge with safari packages, a pool and Tharu-inspired design."),
    ("Green Park Chitwan", "hotel", "Chitwan", "Bagmati", 27.5810, 84.4920, 6000, 4.4,
     ["resort", "pool", "garden"], "Check-in 1:00 PM",
     "Comfortable resort in Sauraha with lush gardens, a pool and organized jungle activities."),

    # ---------------- LUMBINI ----------------
    ("Maya Devi Temple", "attraction", "Lumbini", "Lumbini", 27.4693, 83.2760, 500, 4.7,
     ["unesco", "buddhist", "pilgrimage"], "Daily 6:00 AM - 6:00 PM",
     "The sacred birthplace of Siddhartha Gautama (the Buddha), marked by the Marker Stone and the ancient Ashoka Pillar."),
    ("Lumbini Monastic Zone", "attraction", "Lumbini", "Lumbini", 27.4833, 83.2767, 0, 4.6,
     ["buddhist", "architecture", "peace"], "Daily 6:00 AM - 6:00 PM",
     "A vast peace park where countries have built their own ornate monasteries — explore by bicycle or rickshaw."),
    ("Lumbini Buddha Garden Resort", "hotel", "Lumbini", "Lumbini", 27.4780, 83.2790, 5000, 4.3,
     ["garden", "quiet", "resort"], "Check-in 1:00 PM",
     "Peaceful resort near the monastic zone, ideal for a reflective pilgrimage stay."),

    # ---------------- MUSTANG ----------------
    ("Muktinath Temple", "attraction", "Mustang", "Gandaki", 28.8167, 83.8717, 0, 4.8,
     ["pilgrimage", "hindu", "buddhist", "high-altitude"], "Daily 5:00 AM - 7:00 PM",
     "A revered temple at 3,710m sacred to both Hindus and Buddhists, with 108 water spouts and an eternal flame."),
    ("Kagbeni", "attraction", "Mustang", "Gandaki", 28.8400, 83.7900, 0, 4.6,
     ["village", "trek", "ancient"], "Open all day",
     "A medieval mud-brick village at the gateway to Upper Mustang, with a Tibetan-style monastery and dramatic gorge views."),
    ("Jomsom", "attraction", "Mustang", "Gandaki", 28.7800, 83.7190, 0, 4.5,
     ["trek-hub", "windy-valley", "apple"], "Open all day",
     "Windy administrative hub of Mustang and trailhead for Muktinath; famous for apple orchards and brandy."),

    # ---------------- OTHER CITIES ----------------
    ("Janaki Mandir", "attraction", "Janakpur", "Madhesh", 26.7288, 85.9244, 0, 4.7,
     ["hindu", "heritage", "mithila"], "Daily 6:00 AM - 8:00 PM",
     "A stunning marble Mughal-Rajput temple dedicated to Goddess Sita, the spiritual heart of Mithila culture."),
    ("Dantakali Temple", "attraction", "Dharan", "Koshi", 26.8120, 87.2870, 0, 4.5,
     ["hindu", "shakti-peeth", "hilltop"], "Daily 5:00 AM - 7:00 PM",
     "A hilltop Shakti Peeth temple in Dharan with forested surroundings and city views."),
    ("Kanyam Tea Garden", "attraction", "Ilam", "Koshi", 26.8700, 88.0300, 0, 4.6,
     ["tea", "nature", "viewpoint"], "Open all day",
     "Rolling emerald tea estates in Nepal's eastern hills — walk the rows, sip fresh Ilam tea and soak the views."),
    ("Mai Pokhari", "attraction", "Ilam", "Koshi", 26.9333, 87.9333, 0, 4.4,
     ["lake", "ramsar", "nature"], "Open all day",
     "A serene sacred lake and Ramsar wetland surrounded by forest, rich in orchids and birdlife."),
    ("Siddhababa Temple", "attraction", "Butwal", "Lumbini", 27.7530, 83.4490, 0, 4.3,
     ["hindu", "roadside", "waterfall"], "Daily 5:00 AM - 8:00 PM",
     "A popular roadside temple on the Siddhartha Highway where travelers stop to pray for a safe journey."),
]

# Festivals as discoverable 'events' (city-anchored).
_EVENTS: List[tuple] = [
    ("Indra Jatra", "Kathmandu", "Bagmati", 27.7044, 85.3070, "Sep",
     ["festival", "culture", "kumari"], "Eight-day Kathmandu festival with the living goddess Kumari's chariot procession and masked Lakhe dances."),
    ("Bisket Jatra", "Bhaktapur", "Bagmati", 27.6722, 85.4280, "Apr",
     ["festival", "newari", "newyear"], "Bhaktapur's thrilling New Year chariot festival with tug-of-war and the raising of a giant ceremonial pole."),
    ("Holi (Fagu Purnima)", "Kathmandu", "Bagmati", 27.7151, 85.3110, "Mar",
     ["festival", "colors"], "The festival of colors fills Basantapur and Thamel with water, powder and music."),
    ("Tihar Lights", "Pokhara", "Gandaki", 28.2096, 83.9485, "Oct-Nov",
     ["festival", "lights"], "Lakeside glows with oil lamps, rangoli and Deusi-Bhailo singing during the five-day festival of lights."),
]

EMERGENCY_POIS: List[tuple] = [
    # (name, type, city, lat, lon, phone, address)
    ("Bir Hospital", "hospital", "Kathmandu", 27.7045, 85.3138, "01-4221119", "Mahaboudha, Kathmandu"),
    ("Tribhuvan University Teaching Hospital (TUTH)", "hospital", "Kathmandu", 27.7350, 85.3300, "01-4412303", "Maharajgunj, Kathmandu"),
    ("Norvic International Hospital", "hospital", "Kathmandu", 27.6920, 85.3180, "01-5970032", "Thapathali, Kathmandu"),
    ("Grande International Hospital", "hospital", "Kathmandu", 27.7430, 85.3120, "01-5159266", "Dhapasi, Kathmandu"),
    ("Patan Hospital", "hospital", "Lalitpur", 27.6680, 85.3190, "01-5522295", "Lagankhel, Lalitpur"),
    ("Metropolitan Police Range", "police", "Kathmandu", 27.7030, 85.3130, "01-4226999", "Hanumandhoka, Kathmandu"),
    ("Tourist Police", "police", "Kathmandu", 27.7000, 85.3200, "1144", "Bhrikutimandap, Kathmandu"),
    ("Manipal Teaching Hospital", "hospital", "Pokhara", 28.2280, 83.9870, "061-526416", "Phulbari, Pokhara"),
    ("Western Regional Hospital (Gandaki)", "hospital", "Pokhara", 28.2096, 83.9856, "061-520461", "Ramghat, Pokhara"),
    ("Pokhara Tourist Police", "police", "Pokhara", 28.2100, 83.9800, "061-521087", "Lakeside, Pokhara"),
    ("Bharatpur Hospital", "hospital", "Chitwan", 27.6766, 84.4337, "056-520111", "Bharatpur, Chitwan"),
    ("Lumbini Provincial Hospital (Butwal)", "hospital", "Butwal", 27.7006, 83.4484, "071-420143", "Butwal"),
    ("BP Koirala Institute of Health Sciences", "hospital", "Dharan", 26.8120, 87.2830, "025-525555", "Dharan"),
]


def build_places() -> List[Dict[str, Any]]:
    docs: List[Dict[str, Any]] = []
    counters = {"attraction": 0, "restaurant": 0, "hotel": 0, "event": 0}
    for (name, ptype, city, region, lat, lon, price, rating, tags, hours, desc) in _RAW:
        cat = ptype if ptype in ("restaurant", "hotel") else "heritage"
        if ptype == "attraction":
            cat = "mountain" if any(t in tags for t in ("viewpoint", "lake", "sunrise", "nature", "waterfall", "tea")) else "heritage"
        img = _img(cat, counters.get(ptype, 0))
        counters[ptype] = counters.get(ptype, 0) + 1
        slug = name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("&", "and").replace(".", "").replace(",", "")
        docs.append({
            "id": slug,
            "name": name,
            "type": ptype,
            "city": city,
            "region": region,
            "lat": lat,
            "lon": lon,
            "location": {"type": "Point", "coordinates": [lon, lat]},
            "price_npr": price,
            "rating": rating,
            "tags": tags,
            "hours": hours,
            "description": desc,
            "image_url": img,
            "address": f"{city}, {region}, Nepal",
        })
    # events
    for i, (name, city, region, lat, lon, period, tags, desc) in enumerate(_EVENTS):
        slug = "event-" + name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        docs.append({
            "id": slug,
            "name": name,
            "type": "event",
            "city": city,
            "region": region,
            "lat": lat,
            "lon": lon,
            "location": {"type": "Point", "coordinates": [lon, lat]},
            "price_npr": 0,
            "rating": 4.6,
            "tags": tags,
            "hours": period,
            "period": period,
            "description": desc,
            "image_url": _img("event", i),
            "address": f"{city}, {region}, Nepal",
        })
    return docs


def build_emergency_pois() -> List[Dict[str, Any]]:
    docs = []
    for (name, ptype, city, lat, lon, phone, address) in EMERGENCY_POIS:
        slug = "epoi-" + name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        docs.append({
            "id": slug,
            "name": name,
            "type": ptype,
            "city": city,
            "lat": lat,
            "lon": lon,
            "location": {"type": "Point", "coordinates": [lon, lat]},
            "phone": phone,
            "address": address,
        })
    return docs
