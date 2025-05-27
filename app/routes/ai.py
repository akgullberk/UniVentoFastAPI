from fastapi import APIRouter, HTTPException
from app.models.ai_request import AIRequest
import google.generativeai as genai
from typing import Dict

router = APIRouter()

# Gemini API yapılandırması
GEMINI_API_KEY = "AIzaSyDYTi13XdI7rjbUcwxP7-v0MgjFPoIBX5Q"
genai.configure(api_key=GEMINI_API_KEY)

# Kullanılabilir modelleri listele ve doğru modeli seç
@router.post("/ai/chat")
async def get_ai_response(request: AIRequest) -> Dict[str, str]:
    try:
        # Gemini modelini başlat
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Gemini API'ye istek gönder
        response = model.generate_content(request.prompt)
        
        # Yanıtı kontrol et ve döndür
        if response.text:
            return {
                "status": "success",
                "response": response.text
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="AI yanıt üretemedi"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Bir hata oluştu: {str(e)}"
        ) 