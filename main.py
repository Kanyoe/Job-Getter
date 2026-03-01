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
