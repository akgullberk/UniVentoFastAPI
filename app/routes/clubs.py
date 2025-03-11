from fastapi import APIRouter, HTTPException
from app.db.database import clubs_collection
from app.models.club import Club
from bson import ObjectId

router = APIRouter()

# Tüm kulüpleri getir
@router.get("/clubs")
async def get_clubs():
    clubs = []
    async for club in clubs_collection.find():
        club["_id"] = str(club["_id"])  # ObjectId'yi stringe çeviriyoruz
        clubs.append(club)
    return clubs

# Yeni kulüp ekle
@router.post("/clubs")
async def create_club(club: Club):
    new_club = club.dict()
    result = await clubs_collection.insert_one(new_club)
    return {"id": str(result.inserted_id), "message": "Kulüp başarıyla eklendi"}
