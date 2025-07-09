from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Comment(BaseModel):
    comment_id: Optional[str] = None  # ✅ Make it optional with default None
    post_id: str
    content: str
    file_url: Optional[str] = None
    created_by: Optional[str] = None   # ✅ Make sure this is optional
    created_at: Optional[datetime] = None  # ✅ Same here
