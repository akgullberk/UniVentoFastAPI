from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes.clubs import router as clubs_router

app = FastAPI()

# CORS ayarlarını yapılandırıyoruz
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://16.170.205.160"],  # HTTPS üzerinden sunucu adresi
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP yöntemlerine izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
)

app.include_router(clubs_router)

