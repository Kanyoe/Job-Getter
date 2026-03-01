import os
import shutil
from fastapi import APIRouter, Depends
from some_external_module import SomeDependency  # absolute import

router = APIRouter()

@router.post("/upload_resume")
def upload_resume(file: UploadFile = File(...), some_dependency: SomeDependency = Depends()):
    """ Function to upload a resume and perform cleanup. """
    try:
        # handling the uploaded file
        file_location = f"uploads/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
    finally:
        # cleanup the uploaded file
        if os.path.exists(file_location):
            os.remove(file_location)
        # Optionally, clean up the directory if needed
        shutil.rmtree('uploads') if os.path.isdir('uploads') else None
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil

from utils import extract_text_from_pdf
from database import init_db

app = FastAPI(
    title="Job Getter",
    description="Upload resume → extract text → get job matches (Kenya focused)",
    version="1.0"
)

# CORS (so your frontend can call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change to your domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.on_event("startup")
def startup():
    init_db()
    print("✅ Database initialized")

@app.get("/")
async def root():
    return {"message": "Job Getter API is running! Go to /docs"}

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_location = UPLOAD_DIR / file.filename

    try:
        # Save file temporarily
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Use your utils.py
        extracted_text = extract_text_from_pdf(str(file_location))

        return {
            "status": "success",
            "filename": file.filename,
            "text_length": len(extracted_text),
            "message": "Resume uploaded and text extracted successfully",
            "text_preview": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
        }
    finally:
        # Safe cleanup (only this file)
        if file_location.exists():
            file_location.unlink()
