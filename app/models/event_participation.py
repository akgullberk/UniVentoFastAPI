from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EventParticipation(BaseModel):
    id: Optional[str] = None
    event_id: str
    email: EmailStr  # Kullanıcı e-postası
    status: str = "pending"  # pending, approved, rejected
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    club_president_email: Optional[str] = None  # Kulüp başkanının e-postası
    event_name: Optional[str] = None  # Etkinlik adı 