from pydantic import BaseModel, HttpUrl
from typing import Optional

class Club(BaseModel):
    name: str
    email: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None  # Kulüp logosu
    advisor: Optional[str] = None  # Akademik danışman
    president: Optional[str] = None  # Kulüp başkanı
    category: Optional[str] = None  # Kulüp kolu / türü
