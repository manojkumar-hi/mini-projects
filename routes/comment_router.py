from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Header

from db import db
from models.comment import Comment  # noqa
from utils import decode_jwt_token

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_user(comment: Comment, Authorization: Optional[str] = Header(None)):
    posts_exists = await db.posts.count_documents({"post_id": comment.post_id}) > 0
    if not posts_exists:
        raise HTTPException(status_code=404, detail="Post not found")
    
    user_data = decode_jwt_token(Authorization)

    comment_data = comment.dict()
    comment_data["comment_id"] = str(uuid4())  # Generate a unique comment ID
    comment_data["created_at"] = datetime.now() 
    comment_data["created_by"] = user_data.get("email")  
    
    result = await db.comments.insert_one(comment_data)
    if not result.acknowledged:
        raise HTTPException(
            status_code=500,
            detail="Failed to create comment. Please try again later."
        )
    
    # Ensure created_at is converted to string for JSON response
    created_at_str = comment_data["created_at"].isoformat() if hasattr(comment_data["created_at"], 'isoformat') else str(comment_data["created_at"])
    
    return {
        "status": "success",
        "message": "Comment created successfully",
        "data": {
            "id": str(result.inserted_id),
            "post_id": comment.post_id,
            "content": comment.content,
            "created_by": comment_data["created_by"],
            "created_at": created_at_str
        }
    }

@router.get("/test", response_model=dict)
async def test_endpoint():
    return {"status": "success", "message": "Comment router test endpoint works!"}