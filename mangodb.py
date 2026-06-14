from pymongo import MongoClient

MONGO_URI = "mongodb+srv://gamingvickey126_db_user:vickyda@cluster0.akbq8wy.mongodb.net/"

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True   # ⚠️ avoids SSL issue
)

db = client["resume_analyzer"]
users_collection = db["users"]
resume_collection = db["resumes"]
#lAxPsfCM4QgXidAN