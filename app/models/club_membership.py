from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ClubMembership(BaseModel):
    id: Optional[str] = None
    club_id: str
    member_email: EmailStr
    status: str = "pending"  # pending, approved, rejected
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    club_president_email: Optional[str] = None 