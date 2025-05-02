from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.db.database import events_collection
from app.models.event import Event
from bson import ObjectId
from typing import List, Optional
import aiofiles
import os
from datetime import datetime
import json

router = APIRouter()

# Resim yükleme dizini
UPLOAD_DIR = "uploads/events"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Varsayılan resim URL'i
DEFAULT_IMAGE_URL = "https://www.firat.edu.tr/images/content_menu/16329166375.png"

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

# Yeni etkinlik ekle (resim ile birlikte)
@router.post("/events")
async def create_event(
    name: str = Form(...),
    location: str = Form(...),
    date_time: str = Form(...),
    details: str = Form(...),
    club_id: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    # Etkinlik verilerini oluştur
    event_data = {
        "name": name,
        "location": location,
        "date_time": date_time,
        "details": details,
        "club_id": club_id,
        "image_url": DEFAULT_IMAGE_URL  # Varsayılan resim URL'ini ekle
    }
    
    # Etkinliği veritabanına ekle
    result = await events_collection.insert_one(event_data)
    event_id = str(result.inserted_id)
    
    # Eğer resim yüklendiyse
    if image:
        # Dosya uzantısını kontrol et
        file_extension = image.filename.split(".")[-1].lower()
        if file_extension not in ["jpg", "jpeg", "png", "gif"]:
            # Etkinliği sil ve hata döndür
            await events_collection.delete_one({"_id": ObjectId(event_id)})
            raise HTTPException(status_code=400, detail="Sadece jpg, jpeg, png ve gif dosyaları yüklenebilir")
        
        # Benzersiz dosya adı oluştur
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{event_id}_{timestamp}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Dosyayı kaydet
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await image.read()
            await out_file.write(content)
        
        # Resim URL'ini güncelle
        image_url = f"/uploads/events/{filename}"
        await events_collection.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": {"image_url": image_url}}
        )
    else:
        image_url = DEFAULT_IMAGE_URL
    
    return {
        "id": event_id,
        "message": "Etkinlik başarıyla eklendi",
        "image_url": image_url
    }

# Etkinlik resmi yükle
@router.post("/events/{event_id}/image")
async def upload_event_image(event_id: str, file: UploadFile = File(...)):
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Geçersiz etkinlik ID")
    
    # Etkinliğin var olduğunu kontrol ediyoruz
    existing_event = await events_collection.find_one({"_id": ObjectId(event_id)})
    if not existing_event:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")
    
    # Dosya uzantısını kontrol et
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ["jpg", "jpeg", "png", "gif"]:
        raise HTTPException(status_code=400, detail="Sadece jpg, jpeg, png ve gif dosyaları yüklenebilir")
    
    # Benzersiz dosya adı oluştur
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{event_id}_{timestamp}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Dosyayı kaydet
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # Resim URL'ini güncelle
    image_url = f"/uploads/events/{filename}"
    await events_collection.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": {"image_url": image_url}}
    )
    
    return {"message": "Etkinlik resmi başarıyla yüklendi", "image_url": image_url}

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
    
    # Etkinliğin resmini de sil
    event = await events_collection.find_one({"_id": ObjectId(event_id)})
    if event and "image_url" in event and event["image_url"] != DEFAULT_IMAGE_URL:
        image_path = os.path.join(UPLOAD_DIR, event["image_url"].split("/")[-1])
        if os.path.exists(image_path):
            os.remove(image_path)
    
    result = await events_collection.delete_one({"_id": ObjectId(event_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")
    
    return {"message": "Etkinlik başarıyla silindi"}
