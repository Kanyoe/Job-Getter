from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileIn(BaseModel):
    name: str
    email: EmailStr

class PreferencesIn(BaseModel):
    roles: Optional[str]
    locations: Optional[str]
    remote: Optional[bool]
    min_salary: Optional[int]