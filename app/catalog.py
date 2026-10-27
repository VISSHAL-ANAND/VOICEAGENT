"""Synthetic property and room-type data for development only.

Room labels and prices are fictional examples, not real inventory, quotes, or
availability. The authoritative property-management API must replace these
fixtures before guest-facing use.
"""

LANGUAGES = ["Tamil", "Hindi", "English", "Kannada", "Telugu"]

_DEMO_PROPERTIES = [
    {
        "property_id": "demo-coimbatore-001",
        "name": "Example Garden Stay",
        "city": "Coimbatore",
        "supported_languages": LANGUAGES,
        "amenities": ["Wi-Fi", "Parking", "Family rooms"],
        "room_types": [
            {
                "room_type_id": "demo-coimbatore-standard",
                "name": "Standard Room",
                "max_guests": 2,
                "amenities": ["Wi-Fi", "Air conditioning"],
                "demo_price_per_night_inr": 1800,
                "demo_only": True,
            },
            {
                "room_type_id": "demo-coimbatore-family",
                "name": "Family Room",
                "max_guests": 4,
                "amenities": ["Wi-Fi", "Air conditioning", "Extra beds"],
                "demo_price_per_night_inr": 3200,
                "demo_only": True,
            },
        ],
        "demo_only": True,
    },
    {
        "property_id": "demo-mysuru-001",
        "name": "Example Lake Retreat",
        "city": "Mysuru",
        "supported_languages": LANGUAGES,
        "amenities": ["Garden", "Breakfast area", "Parking"],
        "room_types": [
            {
                "room_type_id": "demo-mysuru-garden",
                "name": "Garden Room",
                "max_guests": 2,
                "amenities": ["Garden view", "Wi-Fi"],
                "demo_price_per_night_inr": 2100,
                "demo_only": True,
            },
            {
                "room_type_id": "demo-mysuru-suite",
                "name": "Family Suite",
                "max_guests": 5,
                "amenities": ["Garden view", "Wi-Fi", "Separate sitting area"],
                "demo_price_per_night_inr": 3900,
                "demo_only": True,
            },
        ],
        "demo_only": True,
    },
    {
        "property_id": "demo-madurai-001",
        "name": "Example Courtyard Home",
        "city": "Madurai",
        "supported_languages": LANGUAGES,
        "amenities": ["Air conditioning", "Family rooms"],
        "room_types": [
            {
                "room_type_id": "demo-madurai-queen",
                "name": "Queen Room",
                "max_guests": 2,
                "amenities": ["Air conditioning", "Wi-Fi"],
                "demo_price_per_night_inr": 1600,
                "demo_only": True,
            },
            {
                "room_type_id": "demo-madurai-family",
                "name": "Courtyard Family Room",
                "max_guests": 4,
                "amenities": ["Air conditioning", "Courtyard access"],
                "demo_price_per_night_inr": 2900,
                "demo_only": True,
            },
        ],
        "demo_only": True,
    },
]


def list_properties(city: str | None = None) -> list[dict]:
    items = _DEMO_PROPERTIES
    if city:
        normalized = city.strip().casefold()
        items = [item for item in items if item["city"].casefold() == normalized]
    return [dict(item) for item in items]


def get_property(property_id: str) -> dict | None:
    for item in _DEMO_PROPERTIES:
        if item["property_id"] == property_id:
            return dict(item)
    return None
