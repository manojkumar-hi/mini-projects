from dataclasses import Field
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from bson import ObjectId as Obj


class Post(BaseModel):
    post_id: Optional[str]   
    type: str
    title: str
    content: str
    file_url: Optional[str] = None
    tags: Optional[List[str]] = None
    created_by: Optional[str] = None   # ✅ Make sure this is optional
    created_at: Optional[datetime] = None  # ✅ Same here
