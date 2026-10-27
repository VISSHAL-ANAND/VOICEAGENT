"""Local-first FastAPI scaffold for VoiceAgent."""

from fastapi import FastAPI, HTTPException, Query

from app.catalog import get_property, list_properties
from app.schemas import HealthResponse, PropertyListResponse, PropertySummary

app = FastAPI(
    title="VoiceAgent API",
    version="0.1.0",
    description="Local prototype. Property records are synthetic; bookings are not enabled.",
)

@app.get("/healthz", response_model=HealthResponse, tags=["operations"])
def health_check() -> HealthResponse:
    return HealthResponse()

@app.get("/api/v1/properties", response_model=PropertyListResponse, tags=["properties"])
def properties(city: str | None = Query(default=None, min_length=1, max_length=100)) -> PropertyListResponse:
    items = [PropertySummary(**item) for item in list_properties(city)]
    return PropertyListResponse(items=items, total=len(items))

@app.get("/api/v1/properties/{property_id}", response_model=PropertySummary, tags=["properties"])
def property_detail(property_id: str) -> PropertySummary:
    item = get_property(property_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertySummary(**item)
