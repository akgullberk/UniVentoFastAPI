from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.clubs import router as clubs_router
from app.routes.events import router as events_router
from app.routes.event_participations import router as event_participations_router
from app.db.database import init_collections

app = FastAPI()

# Statik dosya sunucusu ekle
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS ayarlarını yapılandırıyoruz
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm originlere izin ver
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP yöntemlerine izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
    expose_headers=["*"]  # Tüm başlıkları expose et
)

# Uygulama başladığında koleksiyonları başlat
@app.on_event("startup")
async def startup_db_client():
    await init_collections()

app.include_router(clubs_router)
app.include_router(events_router, prefix="/api", tags=["events"])
app.include_router(event_participations_router, prefix="/api", tags=["event_participations"])

