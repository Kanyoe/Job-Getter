from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import init_db, SessionLocal, UserProfile
from .models import ProfileIn, PreferencesIn
from .utils import extract_text_from_pdf

init_db()
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/profile/")
def create_profile(profile: ProfileIn, db: Session = Depends(get_db)):
    user = UserProfile(name=profile.name, email=profile.email, profile_data={}, preferences={})
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id}

@app.post("/resume/{user_id}")
async def upload_resume(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    content = await file.read()
    with open(f"temp_{user_id}.pdf", "wb") as f:
        f.write(content)
    text = extract_text_from_pdf(f"temp_{user_id}.pdf")
    user.profile_data = {"resume_text": text}
    db.commit()
    return {"message": "Resume uploaded and parsed"}

@app.post("/preferences/{user_id}")
def set_preferences(user_id: int, prefs: PreferencesIn, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.preferences = prefs.dict()
    db.commit()
    return {"message": "Preferences saved"}