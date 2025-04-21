from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional

class Club(BaseModel):
    name: str
    email: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None  # Kulüp logosu
    advisor: Optional[str] = None  # Akademik danışman
    president: Optional[str] = None  # Kulüp başkanı
    president_email: Optional[EmailStr] = None  # Kulüp başkanının e-postası
    president_password: Optional[str] = None  # Kulüp başkanının şifresi
    category: Optional[str] = None  # Kulüp kolu / türü
