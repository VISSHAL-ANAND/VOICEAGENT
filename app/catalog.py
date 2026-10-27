"""Synthetic property data for development only; not live inventory."""

LANGUAGES = ["Tamil", "Hindi", "English", "Kannada", "Telugu"]

_DEMO_PROPERTIES = [
    {
        "property_id": "demo-coimbatore-001",
        "name": "Example Garden Stay",
        "city": "Coimbatore",
        "supported_languages": LANGUAGES,
        "amenities": ["Wi-Fi", "Parking", "Family rooms"],
        "demo_only": True,
    },
    {
        "property_id": "demo-mysuru-001",
        "name": "Example Lake Retreat",
        "city": "Mysuru",
        "supported_languages": LANGUAGES,
        "amenities": ["Garden", "Breakfast area", "Parking"],
        "demo_only": True,
    },
    {
        "property_id": "demo-madurai-001",
        "name": "Example Courtyard Home",
        "city": "Madurai",
        "supported_languages": LANGUAGES,
        "amenities": ["Air conditioning", "Family rooms"],
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
