from pydantic import BaseModel
from typing import Optional

class Club(BaseModel):
    name: str
    description: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
