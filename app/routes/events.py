from fastapi import APIRouter, HTTPException
from app.db.database import events_collection
from app.models.event import Event
from bson import ObjectId
from typing import List

router = APIRouter()

# Tüm etkinlikleri getir
@router.get("/events", response_model=List[Event])
async def get_events():
    events = []
    async for event in events_collection.find():
        event["_id"] = str(event["_id"])
        events.append(event)
    return events

# Belirli bir kulübün etkinliklerini getir
@router.get("/events/club/{club_id}", response_model=List[Event])
async def get_club_events(club_id: str):
    events = []
    async for event in events_collection.find({"club_id": club_id}):
        event["_id"] = str(event["_id"])
        events.append(event)
    return events

# Yeni etkinlik ekle
@router.post("/events")
async def create_event(event: Event):
    new_event = event.dict()
    result = await events_collection.insert_one(new_event)
    return {"id": str(result.inserted_id), "message": "Etkinlik başarıyla eklendi"}

# Etkinlik güncelle
@router.put("/events/{event_id}")
async def update_event(event_id: str, updated_event: Event):
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Geçersiz etkinlik ID")
    
    # Etkinliğin var olduğunu kontrol ediyoruz
    existing_event = await events_collection.find_one({"_id": ObjectId(event_id)})
    if not existing_event:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")
    
    update_data = updated_event.dict(exclude_unset=True)
    result = await events_collection.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Etkinlik güncellenemedi")
    
    return {"message": "Etkinlik başarıyla güncellendi"}

# Etkinlik sil
@router.delete("/events/{event_id}")
async def delete_event(event_id: str):
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Geçersiz etkinlik ID")
    
    result = await events_collection.delete_one({"_id": ObjectId(event_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")
    
    return {"message": "Etkinlik başarıyla silindi"}
