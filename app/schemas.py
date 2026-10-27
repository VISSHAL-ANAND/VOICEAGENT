from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str = 'ok'
    service: str = 'voiceagent-api'
    mode: str = 'local-mock'

class PropertySummary(BaseModel):
    property_id: str
    name: str
    city: str
    supported_languages: list[str]
    amenities: list[str]
    demo_only: bool = True

class PropertyListResponse(BaseModel):
    items: list[PropertySummary]
    total: int
    demo_only: bool = True
