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
uvicorn main:app
import os
import shutil
from fastapi import APIRouter, Depends, File, UploadFile
# You'll need to install a library like: pip install pymupdf
import fitz 

router = APIRouter()

@router.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    
    try:
        # 1. Save the file 
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())

        # 2. EXTRACT TEXT (The missing logic)
        doc = fitz.open(file_location)
        resume_text = ""
        for page in doc:
            resume_text += page.get_text()
        
        # You can now send 'resume_text' to an AI or Keyword Matcher
        return {"filename": file.filename, "status": "Processed", "preview": resume_text[:100]}

    except Exception as e:
        return {"error": str(e)}
        
    finally:
        # 3. Cleanup 
        if os.path.exists(file_location):
            os.remove(file_location) [cite: 1]
        if os.path.isdir('uploads'):
            shutil.rmtree('uploads') [cite: 1]
            
