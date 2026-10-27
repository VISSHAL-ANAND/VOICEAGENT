"""Synthetic property catalog; never represents live inventory or availability."""
from app.schemas import PropertySummary

SUPPORTED_LANGUAGES = ["Tamil", "Hindi", "English", "Kannada", "Telugu"]

# These fictional records are safe development fixtures. Do not use them to quote
# prices, promise availability, or create real reservations.
_DEMO_PROPERTIES = [
    PropertySummary(
        property_id="demo-coimbatore-001",
        name="Example Garden Stay",
        city="Coimbatore",
        supported_languages=SUPPORTED_LANGUAGES,
        amenities=["Wi-Fi", "Parking", "Family rooms"],
    ),
    PropertySummary(
        property_id="demo-mysuru-001",
        name="Example Lake Retreat",
        city="Mysuru",
        supported_languages=SUPPORTED_LANGUAGES,
        amenities=["Garden", "Breakfast area", "Parking"],
    ),
    PropertySummary(
        property_id="demo-madurai-001",
        name="Example Courtyard Home",
        city="Madurai",
        supported_languages=SUPPORTED_LANGUAGES,
        amenities=["Air conditioning", "Family rooms"],
    ),
]


def list_properties(city: str | None = None) -> list[PropertySummary]:
    """Return copied synthetic property summaries, optionally filtered by city."""
    properties = _DEMO_PROPERTIES
    if city:
        normalized_city = city.strip().casefold()
        properties = [p for p in properties if p.city.casefold() == normalized_city]
    return [property.model_copy(deep=True) for property in properties]


def get_property(property_id: str) -> PropertySummary | None:
    """Find one synthetic property by its stable demo identifier."""
    for property in _DEMO_PROPERTIES:
        if property.property_id == property_id:
            return property.model_copy(deep=True)
    return None
