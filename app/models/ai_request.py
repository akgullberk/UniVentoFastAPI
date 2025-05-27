from pydantic import BaseModel

class AIRequest(BaseModel):
    prompt: str  # Kullanıcının gönderdiği metin/soru 