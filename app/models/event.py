from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Event(BaseModel):
    name: str  # Etkinlik adı
    location: str  # Etkinlik konumu
    date_time: str  # Tarih ve saat (string formatında)
    details: str  # Etkinlik detayları
    club_id: Optional[str] = None  # Hangi kulübe ait olduğu (opsiyonel)
    image_url: Optional[str] = None  # Etkinlik resmi URL'i (opsiyonel)
    
    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v)
        } 