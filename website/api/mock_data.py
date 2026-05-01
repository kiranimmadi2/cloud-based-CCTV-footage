import random
from datetime import datetime, timedelta

CAMERA_TYPES = ["PTZ", "Fixed", "Dome", "ANPR", "Speed"]
ZONES = {
    "Bangalore": ["Zone-A Central", "Zone-B North", "Zone-C South", "Zone-D East", "Zone-E West"],
    "Mumbai":    ["Zone-A South", "Zone-B Central", "Zone-C West", "Zone-D North"],
    "Delhi":     ["Zone-A NCR", "Zone-B Central", "Zone-C South", "Zone-D West"],
    "Chennai":   ["Zone-A Central", "Zone-B South", "Zone-C West"],
    "Hyderabad": ["Zone-A Central", "Zone-B West", "Zone-C East"],
}

CLOTHING_OPTIONS = [
    "White shirt, blue jeans",
    "Black hoodie, grey trousers",
    "Dark blue kurta, white pyjama",
    "Grey T-shirt, black cargo pants",
    "Red polo shirt, khaki shorts",
    "Brown jacket, black jeans",
    "Green shirt, dark pants",
    "White shirt, black trousers",
]
DIRECTIONS = ["North", "South", "East", "West", "North-East", "North-West", "South-East", "South-West"]
HEIGHT_OPTIONS = ["5'4\" – 5'6\"", "5'6\" – 5'8\"", "5'8\" – 5'10\"", "5'10\" – 6'0\"", "6'0\" – 6'2\""]
VEHICLE_OPTIONS = [None, None, None, "White sedan (partial plate: KA-05)", "Black motorcycle", "Blue hatchback", "Silver SUV"]

CAMERAS = {
    "Bangalore": [
        {"cam_id":"BLR_001","name":"MG Road & Trinity Circle","address":"MG Road, Near Trinity Circle, Bengaluru 560001","area":"MG Road","zone":"Zone-A Central","type":"PTZ","lat":12.9757,"lng":77.6011,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_002","name":"Brigade Road Main Entry","address":"Brigade Road, Near Church St, Bengaluru 560001","area":"Brigade Road","zone":"Zone-A Central","type":"Fixed","lat":12.9727,"lng":77.6082,"status":"online","resolution":"2K"},
        {"cam_id":"BLR_003","name":"Koramangala 80ft Road Signal","address":"80 Feet Rd, 4th Block, Koramangala, Bengaluru 560034","area":"Koramangala","zone":"Zone-C South","type":"Dome","lat":12.9352,"lng":77.6245,"status":"online","resolution":"1080p"},
        {"cam_id":"BLR_004","name":"Indiranagar 100ft Road","address":"100 Feet Rd, Stage 2, Indiranagar, Bengaluru 560038","area":"Indiranagar","zone":"Zone-D East","type":"PTZ","lat":12.9784,"lng":77.6408,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_005","name":"Whitefield ITPL Gate","address":"ITPL Main Rd, Whitefield, Bengaluru 560066","area":"Whitefield","zone":"Zone-D East","type":"ANPR","lat":12.9698,"lng":77.7500,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_006","name":"Hebbal Flyover East","address":"Hebbal Flyover, NH-44, Bengaluru 560024","area":"Hebbal","zone":"Zone-B North","type":"Speed","lat":13.0358,"lng":77.5970,"status":"online","resolution":"2K"},
        {"cam_id":"BLR_007","name":"Electronic City Phase 1 Gate","address":"Hosur Rd, Electronic City Phase 1, Bengaluru 560100","area":"Electronic City","zone":"Zone-C South","type":"ANPR","lat":12.8456,"lng":77.6603,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_008","name":"Jayanagar 4th Block Circle","address":"4th Block, 11th Main Rd, Jayanagar, Bengaluru 560011","area":"Jayanagar","zone":"Zone-C South","type":"Dome","lat":12.9308,"lng":77.5831,"status":"online","resolution":"1080p"},
        {"cam_id":"BLR_009","name":"Majestic Bus Stand Entrance","address":"Gubbi Thotadappa Rd, Majestic, Bengaluru 560009","area":"Majestic","zone":"Zone-A Central","type":"PTZ","lat":12.9779,"lng":77.5714,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_010","name":"Silk Board Junction","address":"Silk Board Jn, Hosur Rd, Bengaluru 560068","area":"Silk Board","zone":"Zone-C South","type":"PTZ","lat":12.9174,"lng":77.6225,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_011","name":"KR Puram Railway Bridge","address":"Old Madras Rd, KR Puram, Bengaluru 560036","area":"KR Puram","zone":"Zone-D East","type":"Fixed","lat":13.0027,"lng":77.6952,"status":"online","resolution":"2K"},
        {"cam_id":"BLR_012","name":"Bannerghatta Road Toll","address":"Bannerghatta Rd, JP Nagar, Bengaluru 560076","area":"Bannerghatta","zone":"Zone-C South","type":"ANPR","lat":12.8934,"lng":77.5975,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_013","name":"Yelahanka New Town Circle","address":"Doddaballapur Main Rd, Yelahanka, Bengaluru 560064","area":"Yelahanka","zone":"Zone-B North","type":"Dome","lat":13.1005,"lng":77.5963,"status":"online","resolution":"1080p"},
        {"cam_id":"BLR_014","name":"HSR Layout Sector 2","address":"27th Main Rd, HSR Layout, Bengaluru 560102","area":"HSR Layout","zone":"Zone-C South","type":"Fixed","lat":12.9116,"lng":77.6474,"status":"online","resolution":"2K"},
        {"cam_id":"BLR_015","name":"BTM Layout 2nd Stage","address":"2nd Stage, BTM Layout, Bengaluru 560076","area":"BTM Layout","zone":"Zone-C South","type":"Dome","lat":12.9165,"lng":77.6101,"status":"online","resolution":"1080p"},
        {"cam_id":"BLR_016","name":"Marathahalli Bridge West","address":"Outer Ring Rd, Marathahalli, Bengaluru 560037","area":"Marathahalli","zone":"Zone-D East","type":"PTZ","lat":12.9591,"lng":77.7010,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_017","name":"Domlur Flyover Junction","address":"Airport Rd, Domlur, Bengaluru 560071","area":"Domlur","zone":"Zone-D East","type":"Speed","lat":12.9609,"lng":77.6387,"status":"online","resolution":"2K"},
        {"cam_id":"BLR_018","name":"Richmond Circle","address":"Richmond Rd, Shanthala Nagar, Bengaluru 560025","area":"Richmond Town","zone":"Zone-A Central","type":"PTZ","lat":12.9626,"lng":77.5951,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_019","name":"Rajajinagar 3rd Block","address":"3rd Block, Rajajinagar, Bengaluru 560010","area":"Rajajinagar","zone":"Zone-E West","type":"Fixed","lat":12.9999,"lng":77.5544,"status":"online","resolution":"2K"},
        {"cam_id":"BLR_020","name":"Yeshwanthpur Circle","address":"Tumkur Rd, Yeshwanthpur, Bengaluru 560022","area":"Yeshwanthpur","zone":"Zone-E West","type":"ANPR","lat":13.0218,"lng":77.5468,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_021","name":"Bellandur Lake Gate","address":"Outer Ring Rd, Bellandur, Bengaluru 560103","area":"Bellandur","zone":"Zone-D East","type":"PTZ","lat":12.9256,"lng":77.6763,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_022","name":"Sarjapur Road Signal","address":"Sarjapur Rd, Carmelaram, Bengaluru 560035","area":"Sarjapur","zone":"Zone-D East","type":"Dome","lat":12.9078,"lng":77.6827,"status":"online","resolution":"1080p"},
        {"cam_id":"BLR_023","name":"Nagawara Flyover North","address":"HBR Layout, Nagawara, Bengaluru 560045","area":"Nagawara","zone":"Zone-B North","type":"Speed","lat":13.0457,"lng":77.6184,"status":"online","resolution":"2K"},
        {"cam_id":"BLR_024","name":"Kengeri Bus Terminal","address":"Mysore Rd, Kengeri, Bengaluru 560060","area":"Kengeri","zone":"Zone-E West","type":"ANPR","lat":12.9079,"lng":77.4823,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_025","name":"Banashankari Temple Road","address":"BSK 2nd Stage, Banashankari, Bengaluru 560070","area":"Banashankari","zone":"Zone-C South","type":"Fixed","lat":12.9255,"lng":77.5468,"status":"online","resolution":"1080p"},
        {"cam_id":"BLR_026","name":"Ulsoor Lake Junction","address":"Ulsoor Rd, Bengaluru 560042","area":"Ulsoor","zone":"Zone-A Central","type":"PTZ","lat":12.9833,"lng":77.6204,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_027","name":"Shivajinagar Bus Stand","address":"Shivajinagar, Bengaluru 560001","area":"Shivajinagar","zone":"Zone-A Central","type":"Dome","lat":12.9848,"lng":77.5988,"status":"online","resolution":"2K"},
        {"cam_id":"BLR_028","name":"Cunningham Road","address":"Cunningham Rd, Vasanth Nagar, Bengaluru 560052","area":"Vasanth Nagar","zone":"Zone-A Central","type":"Fixed","lat":12.9939,"lng":77.5927,"status":"online","resolution":"1080p"},
        {"cam_id":"BLR_029","name":"Hebbal Lake Bridge","address":"Hebbal Lake, Bengaluru 560024","area":"Hebbal","zone":"Zone-B North","type":"PTZ","lat":13.0462,"lng":77.5914,"status":"maintenance","resolution":"4K"},
        {"cam_id":"BLR_030","name":"Mysore Road NICE Junction","address":"Mysore Rd, NICE Rd Jn, Bengaluru 560026","area":"Mysore Road","zone":"Zone-E West","type":"ANPR","lat":12.9428,"lng":77.5122,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_031","name":"Jalahalli Cross","address":"Tumkur Rd, Jalahalli Cross, Bengaluru 560013","area":"Jalahalli","zone":"Zone-B North","type":"Speed","lat":13.0306,"lng":77.5299,"status":"online","resolution":"2K"},
        {"cam_id":"BLR_032","name":"Bannerghatta Jigani Road","address":"Jigani Main Rd, Bengaluru 560083","area":"Jigani","zone":"Zone-C South","type":"Fixed","lat":12.8617,"lng":77.6137,"status":"online","resolution":"1080p"},
        {"cam_id":"BLR_033","name":"HAL Airport Road","address":"Old Airport Rd, Varthur, Bengaluru 560017","area":"HAL","zone":"Zone-D East","type":"ANPR","lat":12.9613,"lng":77.6640,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_034","name":"Tumkur Road NH-4","address":"NH-4, Peenya, Bengaluru 560058","area":"Peenya","zone":"Zone-E West","type":"Speed","lat":13.0274,"lng":77.5151,"status":"online","resolution":"4K"},
        {"cam_id":"BLR_035","name":"Hosur Road Begur","address":"Hosur Rd, Begur, Bengaluru 560068","area":"Begur","zone":"Zone-C South","type":"Fixed","lat":12.8912,"lng":77.6350,"status":"online","resolution":"2K"},
    ],
    "Mumbai": [
        {"cam_id":"MUM_001","name":"Dadar TT Circle","address":"Tilak Bridge, Dadar East, Mumbai 400014","area":"Dadar","zone":"Zone-B Central","type":"PTZ","lat":19.0178,"lng":72.8478,"status":"online","resolution":"4K"},
        {"cam_id":"MUM_002","name":"Andheri Station West Entry","address":"Veera Desai Rd, Andheri West, Mumbai 400058","area":"Andheri","zone":"Zone-D North","type":"Fixed","lat":19.1197,"lng":72.8468,"status":"online","resolution":"2K"},
        {"cam_id":"MUM_003","name":"Bandra Bandstand Road","address":"Bandstand, Bandra West, Mumbai 400050","area":"Bandra","zone":"Zone-C West","type":"PTZ","lat":19.0543,"lng":72.8183,"status":"online","resolution":"4K"},
        {"cam_id":"MUM_004","name":"Kurla Station East","address":"LBS Rd, Kurla East, Mumbai 400024","area":"Kurla","zone":"Zone-B Central","type":"Dome","lat":19.0726,"lng":72.8795,"status":"online","resolution":"1080p"},
        {"cam_id":"MUM_005","name":"Borivali National Park Gate","address":"Western Express Hwy, Borivali East, Mumbai 400066","area":"Borivali","zone":"Zone-D North","type":"ANPR","lat":19.2288,"lng":72.8655,"status":"online","resolution":"4K"},
        {"cam_id":"MUM_006","name":"Thane Station East Gate","address":"Station Rd, Thane West 400601","area":"Thane","zone":"Zone-D North","type":"PTZ","lat":19.1863,"lng":72.9707,"status":"online","resolution":"4K"},
        {"cam_id":"MUM_007","name":"Chembur Monorail Station","address":"Eastern Express Hwy, Chembur, Mumbai 400071","area":"Chembur","zone":"Zone-B Central","type":"Dome","lat":19.0622,"lng":72.9005,"status":"online","resolution":"2K"},
        {"cam_id":"MUM_008","name":"Powai Lake Road","address":"Adi Shankaracharya Marg, Powai, Mumbai 400076","area":"Powai","zone":"Zone-D North","type":"Fixed","lat":19.1197,"lng":72.9051,"status":"online","resolution":"2K"},
        {"cam_id":"MUM_009","name":"Worli Sea Face","address":"Dr Annie Besant Rd, Worli, Mumbai 400018","area":"Worli","zone":"Zone-A South","type":"PTZ","lat":19.0109,"lng":72.8178,"status":"online","resolution":"4K"},
        {"cam_id":"MUM_010","name":"Vashi Navi Mumbai Entry","address":"Sion-Panvel Hwy, Vashi, Navi Mumbai 400703","area":"Vashi","zone":"Zone-B Central","type":"ANPR","lat":19.0771,"lng":73.0102,"status":"online","resolution":"4K"},
        {"cam_id":"MUM_011","name":"Ghatkopar Metro Station","address":"LBS Marg, Ghatkopar East, Mumbai 400077","area":"Ghatkopar","zone":"Zone-B Central","type":"Speed","lat":19.0863,"lng":72.9087,"status":"online","resolution":"2K"},
        {"cam_id":"MUM_012","name":"CST Station Entrance","address":"Chhatrapati Shivaji Maharaj Terminus, Mumbai 400001","area":"Fort","zone":"Zone-A South","type":"PTZ","lat":18.9399,"lng":72.8354,"status":"online","resolution":"4K"},
    ],
    "Delhi": [
        {"cam_id":"DEL_001","name":"Connaught Place Inner Circle","address":"Connaught Place, New Delhi 110001","area":"Connaught Place","zone":"Zone-B Central","type":"PTZ","lat":28.6315,"lng":77.2167,"status":"online","resolution":"4K"},
        {"cam_id":"DEL_002","name":"Karol Bagh Ajmal Khan Rd","address":"Ajmal Khan Rd, Karol Bagh, New Delhi 110005","area":"Karol Bagh","zone":"Zone-B Central","type":"Fixed","lat":28.6513,"lng":77.1902,"status":"online","resolution":"2K"},
        {"cam_id":"DEL_003","name":"Lajpat Nagar Central Market","address":"Central Market, Lajpat Nagar II, New Delhi 110024","area":"Lajpat Nagar","zone":"Zone-C South","type":"Dome","lat":28.5672,"lng":77.2434,"status":"online","resolution":"1080p"},
        {"cam_id":"DEL_004","name":"Dwarka Sector 10 Metro","address":"Dwarka Sector 10 Metro Station, New Delhi 110075","area":"Dwarka","zone":"Zone-A NCR","type":"ANPR","lat":28.5921,"lng":77.0460,"status":"online","resolution":"4K"},
        {"cam_id":"DEL_005","name":"Rohini Sector 3 Main","address":"Sector 3, Rohini, New Delhi 110085","area":"Rohini","zone":"Zone-D West","type":"PTZ","lat":28.7195,"lng":77.1282,"status":"online","resolution":"4K"},
        {"cam_id":"DEL_006","name":"Saket Select Citywalk Gate","address":"Press Enclave Rd, Saket, New Delhi 110017","area":"Saket","zone":"Zone-C South","type":"Dome","lat":28.5245,"lng":77.2066,"status":"online","resolution":"2K"},
        {"cam_id":"DEL_007","name":"Nehru Place Crossing","address":"Nehru Place, New Delhi 110019","area":"Nehru Place","zone":"Zone-C South","type":"Fixed","lat":28.5491,"lng":77.2508,"status":"online","resolution":"2K"},
        {"cam_id":"DEL_008","name":"India Gate C-Hexagon","address":"India Gate, Rajpath, New Delhi 110001","area":"India Gate","zone":"Zone-B Central","type":"PTZ","lat":28.6129,"lng":77.2295,"status":"online","resolution":"4K"},
        {"cam_id":"DEL_009","name":"IGI Airport Terminal 3","address":"Terminal 3, IGI Airport, New Delhi 110037","area":"IGI Airport","zone":"Zone-D West","type":"ANPR","lat":28.5572,"lng":77.0896,"status":"online","resolution":"4K"},
        {"cam_id":"DEL_010","name":"Chandni Chowk Main Road","address":"Chandni Chowk, Old Delhi 110006","area":"Chandni Chowk","zone":"Zone-B Central","type":"Speed","lat":28.6505,"lng":77.2303,"status":"online","resolution":"2K"},
    ],
    "Chennai": [
        {"cam_id":"CHN_001","name":"T Nagar Pondy Bazaar","address":"Pondy Bazaar, T Nagar, Chennai 600017","area":"T Nagar","zone":"Zone-A Central","type":"PTZ","lat":13.0418,"lng":80.2341,"status":"online","resolution":"4K"},
        {"cam_id":"CHN_002","name":"Anna Nagar 2nd Avenue","address":"2nd Ave, Anna Nagar, Chennai 600040","area":"Anna Nagar","zone":"Zone-B South","type":"Fixed","lat":13.0850,"lng":80.2101,"status":"online","resolution":"2K"},
        {"cam_id":"CHN_003","name":"Adyar Lattice Bridge","address":"Lattice Bridge Rd, Adyar, Chennai 600020","area":"Adyar","zone":"Zone-B South","type":"Dome","lat":13.0012,"lng":80.2565,"status":"online","resolution":"1080p"},
        {"cam_id":"CHN_004","name":"Velachery Vijayanagar","address":"Vijayanagar, Velachery, Chennai 600042","area":"Velachery","zone":"Zone-B South","type":"ANPR","lat":12.9815,"lng":80.2209,"status":"online","resolution":"4K"},
        {"cam_id":"CHN_005","name":"Tambaram Bus Junction","address":"Grand Southern Trunk Rd, Tambaram, Chennai 600045","area":"Tambaram","zone":"Zone-C West","type":"Speed","lat":12.9249,"lng":80.1000,"status":"online","resolution":"2K"},
        {"cam_id":"CHN_006","name":"Porur OMR Toll","address":"OMR, Porur, Chennai 600116","area":"Porur","zone":"Zone-C West","type":"ANPR","lat":13.0343,"lng":80.1571,"status":"online","resolution":"4K"},
        {"cam_id":"CHN_007","name":"Central Station Entry","address":"Chennai Central, Park Town, Chennai 600003","area":"Park Town","zone":"Zone-A Central","type":"PTZ","lat":13.0827,"lng":80.2707,"status":"online","resolution":"4K"},
        {"cam_id":"CHN_008","name":"Koyambedu Bus Terminus","address":"Koyambedu, Chennai 600107","area":"Koyambedu","zone":"Zone-C West","type":"Dome","lat":13.0684,"lng":80.1935,"status":"online","resolution":"2K"},
    ],
    "Hyderabad": [
        {"cam_id":"HYD_001","name":"Hitech City HUDA Gate","address":"HUDA Techno Enclave, Hitech City, Hyderabad 500081","area":"Hitech City","zone":"Zone-B West","type":"PTZ","lat":17.4435,"lng":78.3772,"status":"online","resolution":"4K"},
        {"cam_id":"HYD_002","name":"Banjara Hills Road No 12","address":"Road No 12, Banjara Hills, Hyderabad 500034","area":"Banjara Hills","zone":"Zone-A Central","type":"Fixed","lat":17.4156,"lng":78.4347,"status":"online","resolution":"2K"},
        {"cam_id":"HYD_003","name":"Secunderabad Station East","address":"Station Rd, Secunderabad 500003","area":"Secunderabad","zone":"Zone-A Central","type":"Dome","lat":17.4399,"lng":78.4983,"status":"online","resolution":"1080p"},
        {"cam_id":"HYD_004","name":"Gachibowli Signal","address":"Gachibowli, Financial District, Hyderabad 500032","area":"Gachibowli","zone":"Zone-B West","type":"ANPR","lat":17.4401,"lng":78.3489,"status":"online","resolution":"4K"},
        {"cam_id":"HYD_005","name":"LB Nagar X Roads","address":"LB Nagar, Hyderabad 500074","area":"LB Nagar","zone":"Zone-C East","type":"Speed","lat":17.3472,"lng":78.5529,"status":"online","resolution":"2K"},
        {"cam_id":"HYD_006","name":"Ameerpet Metro Junction","address":"Ameerpet, Hyderabad 500016","area":"Ameerpet","zone":"Zone-A Central","type":"PTZ","lat":17.4374,"lng":78.4487,"status":"online","resolution":"4K"},
        {"cam_id":"HYD_007","name":"Charminar Entry Gate","address":"Charminar Rd, Old City, Hyderabad 500002","area":"Old City","zone":"Zone-C East","type":"Fixed","lat":17.3616,"lng":78.4747,"status":"online","resolution":"2K"},
        {"cam_id":"HYD_008","name":"RGIA Airport Exit","address":"Rajiv Gandhi International Airport, Shamshabad 501218","area":"Shamshabad","zone":"Zone-B West","type":"ANPR","lat":17.2403,"lng":78.4294,"status":"online","resolution":"4K"},
    ],
}

CITY_CENTERS = {
    "Bangalore": {"lat": 12.9716, "lng": 77.5946, "zoom": 12},
    "Mumbai":    {"lat": 19.0760, "lng": 72.8777, "zoom": 12},
    "Delhi":     {"lat": 28.6139, "lng": 77.2090, "zoom": 12},
    "Chennai":   {"lat": 13.0827, "lng": 80.2707, "zoom": 12},
    "Hyderabad": {"lat": 17.3850, "lng": 78.4867, "zoom": 12},
}

CITY_STATS = {
    "Bangalore": {"total_cams": 2847, "active_cases": 18, "alerts_today": 7},
    "Mumbai":    {"total_cams": 3412, "active_cases": 31, "alerts_today": 12},
    "Delhi":     {"total_cams": 4100, "active_cases": 27, "alerts_today": 9},
    "Chennai":   {"total_cams": 1983, "active_cases": 14, "alerts_today": 5},
    "Hyderabad": {"total_cams": 2210, "active_cases": 22, "alerts_today": 8},
}


def get_cameras(city: str):
    return CAMERAS.get(city, [])


def get_city_stats(city: str):
    return CITY_STATS.get(city, {"total_cams": 1000, "active_cases": 10, "alerts_today": 3})


def _alert_level(confidence: float) -> str:
    if confidence >= 0.90:
        return "CRITICAL"
    elif confidence >= 0.82:
        return "HIGH"
    elif confidence >= 0.74:
        return "MEDIUM"
    return "LOW"


def generate_search_results(city: str, start_dt: datetime, end_dt: datetime):
    cams = CAMERAS.get(city, [])
    if not cams:
        return []

    num_hits = random.randint(5, min(9, len(cams)))
    selected = random.sample(cams, num_hits)

    total_seconds = int((end_dt - start_dt).total_seconds())
    if total_seconds <= 0:
        total_seconds = 3600

    clothing = random.choice(CLOTHING_OPTIONS)
    height = random.choice(HEIGHT_OPTIONS)

    results = []
    used_offsets = set()
    for cam in selected:
        for _ in range(100):
            offset = random.randint(0, total_seconds)
            if all(abs(offset - u) > 240 for u in used_offsets):
                used_offsets.add(offset)
                break
        ts = start_dt + timedelta(seconds=offset)
        confidence = round(random.uniform(0.71, 0.97), 2)
        vehicle = random.choice(VEHICLE_OPTIONS)
        results.append({
            "cam_id": cam["cam_id"],
            "cam_name": cam["name"],
            "address": cam["address"],
            "area": cam["area"],
            "zone": cam["zone"],
            "cam_type": cam["type"],
            "lat": cam["lat"],
            "lng": cam["lng"],
            "timestamp": ts.isoformat(),
            "confidence": confidence,
            "alert_level": _alert_level(confidence),
            "direction": random.choice(DIRECTIONS),
            "clothing": clothing,
            "height_est": height,
            "vehicle": vehicle,
            "snapshot_url": f"https://picsum.photos/seed/{cam['cam_id']}/400/225",
            "face_crop_url": f"https://picsum.photos/seed/{cam['cam_id']}face/80/80",
        })

    results.sort(key=lambda x: x["timestamp"])
    for i, r in enumerate(results):
        r["order"] = i + 1

    return results
