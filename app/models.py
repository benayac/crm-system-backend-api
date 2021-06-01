from pydantic import BaseModel

class ReportModel(BaseModel):
    category: str
    subcategory: str
    description: str
    latitude: float
    longitude: float
    img_url: str