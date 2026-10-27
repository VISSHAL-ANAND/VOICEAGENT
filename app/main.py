from fastapi import FastAPI, HTTPException
from app.catalog import get_property, list_properties

app = FastAPI(title="VoiceAgent API", version="0.1.0", description="Local prototype using synthetic property data only.")

@app.get("/healthz")
def health_check():
    return {"status": "ok", "service": "voiceagent-api", "mode": "local-mock"}

@app.get("/api/v1/properties")
def properties(city: str = None):
    items = list_properties(city)
    return {"items": items, "total": len(items), "demo_only": True}

@app.get("/api/v1/properties/{property_id}")
def property_detail(property_id: str):
    item = get_property(property_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return item
