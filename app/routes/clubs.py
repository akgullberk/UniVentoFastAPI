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


# Kulüp güncelleme
@router.put("/clubs/{club_id}")
async def update_club(club_id: str, updated_club: Club):
    if not ObjectId.is_valid(club_id):
        raise HTTPException(status_code=400, detail="Geçersiz ID")

    update_data = updated_club.dict(exclude_unset=True)
    result = await clubs_collection.update_one({"_id": ObjectId(club_id)}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Kulüp bulunamadı veya güncellenmedi")

    return {"message": "Kulüp başarıyla güncellendi"}