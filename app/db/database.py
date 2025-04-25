import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]
clubs_collection = database.get_collection("clubs")  # Koleksiyon (tablo gibi)
events_collection = database.get_collection("events")  # Etkinlikler koleksiyonu
