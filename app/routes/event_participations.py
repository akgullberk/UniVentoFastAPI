from fastapi import APIRouter, HTTPException, Form, Request
from app.db.database import event_participations_collection, events_collection, clubs_collection
from app.models.event_participation import EventParticipation
from typing import List
from datetime import datetime
import uuid
from bson import ObjectId
from fastapi.responses import JSONResponse
from bson.errors import InvalidId

router = APIRouter()

# Debug: Tüm katılım isteklerini göster
@router.get("/events/participations/debug")
async def get_participations_debug():
    participations = []
    async for participation in event_participations_collection.find():
        participation["_id"] = str(participation["_id"])
        participations.append(participation)
    return participations

# Etkinliğe katılım isteği gönder
@router.post("/events/{event_id}/participate")
async def create_participation_request(
    request: Request,
    event_id: str,
    email: str = Form(...)
):
    try:
        # Debug bilgisi
        print(f"Gelen istek - Event ID: {event_id}, Email: {email}")
        
        # ObjectId dönüşümünü kontrol et
        try:
            event_object_id = ObjectId(event_id)
        except InvalidId:
            return JSONResponse(
                status_code=400,
                content={"detail": "Geçersiz etkinlik ID formatı. 24 karakterlik hexadecimal string olmalıdır."}
            )
        
        # Etkinliğin var olduğunu kontrol et
        event = await events_collection.find_one({"_id": event_object_id})
        if not event:
            print(f"Etkinlik bulunamadı - ID: {event_id}")
            return JSONResponse(
                status_code=404,
                content={"detail": f"Etkinlik bulunamadı. ID: {event_id}"}
            )
        
        # Daha önce istek gönderilmiş mi kontrol et
        existing_request = await event_participations_collection.find_one({
            "event_id": str(event_object_id),
            "email": email
        })
        if existing_request:
            return JSONResponse(
                status_code=400,
                content={"detail": "Bu etkinlik için zaten bir katılım isteğiniz bulunmakta"}
            )
        
        # Kulüp başkanının e-postasını al
        club_president_email = None
        if event.get("club_id"):
            try:
                club = await clubs_collection.find_one({"_id": ObjectId(event["club_id"])})
                if club:
                    club_president_email = club.get("president_email")
            except InvalidId:
                print(f"Geçersiz kulüp ID'si: {event['club_id']}")
        
        # Katılım isteği oluştur
        participation = EventParticipation(
            id=str(uuid.uuid4()),
            event_id=str(event_object_id),
            email=email,
            club_president_email=club_president_email,
            event_name=event.get("name", "Bilinmeyen Etkinlik")
        )
        
        result = await event_participations_collection.insert_one(participation.dict())
        print(f"Katılım isteği oluşturuldu - ID: {result.inserted_id}")
        
        return JSONResponse(
            status_code=200,
            content={"message": "Katılım isteği başarıyla gönderildi", "id": str(result.inserted_id)}
        )
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Bir hata oluştu: {str(e)}"}
        )

# Kulüp başkanının katılım isteklerini görüntülemesi
@router.get("/events/participation-requests/{club_president_email}", response_model=List[EventParticipation])
async def get_participation_requests(club_president_email: str):
    requests = []
    async for request in event_participations_collection.find({"club_president_email": club_president_email}):
        # Etkinlik bilgilerini al
        event = await events_collection.find_one({"_id": ObjectId(request["event_id"])})
        if event:
            request["event_name"] = event.get("name", "Bilinmeyen Etkinlik")
        request["id"] = str(request["_id"])
        requests.append(request)
    return requests

# Katılım isteğini onayla veya reddet
@router.put("/events/participation-requests/{request_id}")
async def update_participation_request(request_id: str, status: str):
    if status not in ["approved", "rejected"]:
        return JSONResponse(
            status_code=400,
            content={"detail": "Geçersiz durum. 'approved' veya 'rejected' olmalıdır."}
        )
    
    result = await event_participations_collection.update_one(
        {"_id": ObjectId(request_id)},
        {
            "$set": {
                "status": status,
                "updated_at": datetime.now()
            }
        }
    )
    
    if result.modified_count == 0:
        return JSONResponse(
            status_code=404,
            content={"detail": "Katılım isteği bulunamadı"}
        )
    
    return JSONResponse(
        status_code=200,
        content={"message": f"Katılım isteği {status} olarak güncellendi"}
    )

# Kullanıcının katılım isteklerini görüntülemesi
@router.get("/events/my-participations/{email}", response_model=List[EventParticipation])
async def get_user_participations(email: str):
    requests = []
    async for request in event_participations_collection.find({"email": email}):
        # Etkinlik bilgilerini al
        event = await events_collection.find_one({"_id": ObjectId(request["event_id"])})
        if event:
            request["event_name"] = event.get("name", "Bilinmeyen Etkinlik")
        request["id"] = str(request["_id"])
        requests.append(request)
    return requests 