from fastapi import FastAPI, UploadFile, File, Form
import os
import shutil
from auth import signup, login
from mangodb import resume_collection
from model import compare_resumes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS so Streamlit (port 10000) can talk to FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Safety Check: Force Python to create the uploads folder immediately on startup
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/signup")
async def signup_api(username: str = Form(...), password: str = Form(...), role: str = Form(...)):
    return signup(username, password, role)

@app.post("/login")
async def login_api(username: str = Form(...), password: str = Form(...)):
    return login(username, password)

@app.post("/upload_student")
async def upload_student(username: str = Form(...), file: UploadFile = File(...)):
    # Save the file securely inside our newly guaranteed uploads folder
    path = f"{UPLOAD_DIR}/{username}_{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Upsert: Update if exists, Insert if new
    resume_collection.update_one(
        {"username": username, "type": "student"},
        {"$set": {"username": username, "type": "student", "path": path}},
        upsert=True
    )
    return {"message": "Student resume uploaded successfully"}

@app.post("/upload_admin")
async def upload_admin(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/admin_{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    resume_collection.update_one(
        {"type": "admin"},
        {"$set": {"type": "admin", "path": path}},
        upsert=True
    )
    return {"message": "Admin resume updated successfully"}

@app.post("/compare")
async def compare(username: str = Form(...)):
    # Fetch paths from the database
    student = resume_collection.find_one({"username": username, "type": "student"})
    admin = resume_collection.find_one({"type": "admin"})
    
    if not student or not admin:
        return {"error": "Missing resumes"}
        
    # Send paths to the NLP model for analysis
    result = compare_resumes(student["path"], admin["path"])
    return result