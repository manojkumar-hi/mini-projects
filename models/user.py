from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_id: Optional[str]
    name: str
    email: str  
    bio: str = None
    # profile_picture: str = None
    password: str

class UserLogin(BaseModel):  # Change to UserLogin (capital U)
    email: str
    password: str