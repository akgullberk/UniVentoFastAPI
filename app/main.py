from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.clubs import router as clubs_router
from app.routes.events import router as events_router

app = FastAPI()

# CORS ayarlarını yapılandırıyoruz
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://16.170.205.160"],  # HTTPS üzerinden sunucu adresi
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP yöntemlerine izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
)

# Statik dosya sunucusu ekle
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(clubs_router)
app.include_router(events_router, prefix="/api", tags=["events"])

