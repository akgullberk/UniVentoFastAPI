from fastapi import APIRouter, HTTPException, Form
from app.db.database import clubs_collection, club_memberships_collection
from app.models.club_membership import ClubMembership
from typing import List
from datetime import datetime
import uuid
from bson import ObjectId

router = APIRouter()

# Kulübe üyelik başvurusu yap
@router.post("/clubs/{club_id}/join")
async def join_club(
    club_id: str,
    email: str = Form(...)
):
    try:
        # Kulübün var olduğunu kontrol et
        club = await clubs_collection.find_one({"_id": ObjectId(club_id)})
        if not club:
            return {"status_code": 404, "detail": "Kulüp bulunamadı"}
        
        # Daha önce başvuru yapılmış mı kontrol et
        existing_membership = await club_memberships_collection.find_one({
            "club_id": club_id,
            "member_email": email
        })
        if existing_membership:
            return {"status_code": 400, "detail": "Bu kulübe zaten üyelik başvurunuz bulunmakta"}
        
        # Üyelik başvurusu oluştur
        membership = ClubMembership(
            id=str(uuid.uuid4()),
            club_id=club_id,
            member_email=email,
            club_president_email=club.get("president_email")
        )
        
        result = await club_memberships_collection.insert_one(membership.dict())
        
        return {
            "status_code": 200,
            "message": "Üyelik başvurunuz başarıyla alındı",
            "id": str(result.inserted_id)
        }
    except Exception as e:
        return {"status_code": 500, "detail": f"Bir hata oluştu: {str(e)}"}

# Kulüp başkanının bekleyen üyelik başvurularını görüntülemesi
@router.get("/clubs/membership-requests/{club_president_email}", response_model=List[ClubMembership])
async def get_membership_requests(club_president_email: str):
    requests = []
    async for request in club_memberships_collection.find({"club_president_email": club_president_email}):
        request["id"] = str(request["_id"])
        requests.append(request)
    return requests

# Üyelik başvurusunu onayla veya reddet
@router.put("/clubs/membership-requests/{request_id}")
async def update_membership_request(request_id: str, status: str):
    if status not in ["approved", "rejected"]:
        return {"status_code": 400, "detail": "Geçersiz durum. 'approved' veya 'rejected' olmalıdır"}
    
    result = await club_memberships_collection.update_one(
        {"_id": ObjectId(request_id)},
        {
            "$set": {
                "status": status,
                "updated_at": datetime.now()
            }
        }
    )
    
    if result.modified_count == 0:
        return {"status_code": 404, "detail": "Üyelik başvurusu bulunamadı"}
    
    return {
        "status_code": 200,
        "message": f"Üyelik başvurusu {status} olarak güncellendi"
    }

# Kullanıcının üyelik başvurularını görüntülemesi
@router.get("/clubs/my-memberships/{email}", response_model=List[ClubMembership])
async def get_user_memberships(email: str):
    memberships = []
    async for membership in club_memberships_collection.find({"member_email": email}):
        membership["id"] = str(membership["_id"])
        memberships.append(membership)
    return memberships 