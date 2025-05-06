import motor.motor_asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]
clubs_collection = database.get_collection("clubs")  # Koleksiyon (tablo gibi)
events_collection = database.get_collection("events")  # Etkinlikler koleksiyonu
event_participations_collection = database.get_collection("event_participations")  # Etkinlik katılım istekleri koleksiyonu

# Koleksiyonun varlığını kontrol et ve yoksa oluştur
async def init_collections():
    # event_participations koleksiyonunu kontrol et
    collections = await database.list_collection_names()
    if "event_participations" not in collections:
        # Test verisi ekle
        test_participation = {
            "_id": "test_participation",
            "event_id": "test_event",
            "email": "test@example.com",
            "status": "pending",
            "created_at": datetime.now(),
            "club_president_id": None
        }
        await event_participations_collection.insert_one(test_participation)
        # Test verisini sil
        await event_participations_collection.delete_one({"_id": "test_participation"})
        print("event_participations koleksiyonu oluşturuldu")
