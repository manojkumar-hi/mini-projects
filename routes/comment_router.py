from datetime import datetime
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Header, Path
from pydantic import BaseModel
from db import db
from models.comment import Comment  # noqa
from utils import decode_jwt_token

class CommentRequest(BaseModel):
    content: str

router = APIRouter()

@router.post("/posts/{post_id}/comments", response_model=dict)
async def create_comment(
    comment: CommentRequest,
    post_id: str = Path(..., description="The ID of the post to comment on"),
    Authorization: Optional[str] = Header(None)
):
    # Check if post exists
    posts_exists = await db.posts.count_documents({"post_id": post_id}) > 0
    if not posts_exists:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Decode user from JWT
    user_data = decode_jwt_token(Authorization)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    # Prepare comment data
    comment_data = comment.dict()
    comment_data["comment_id"] = str(uuid4())
    comment_data["created_at"] = datetime.now()
    comment_data["created_by"] = user_data.get("email")
    comment_data["post_id"] = post_id  # Ensure post_id is set from path

    # Insert comment
    result = await db.comments.insert_one(comment_data)
    if not result.acknowledged:
        raise HTTPException(
            status_code=500,
            detail="Failed to create comment. Please try again later."
        )

    # Prepare response
    created_at_str = comment_data["created_at"].isoformat() if hasattr(comment_data["created_at"], 'isoformat') else str(comment_data["created_at"])
    return {
        "status": "success",
        "message": "Comment created successfully",
        "data": {
            "id": str(result.inserted_id),
            "comment_id": comment_data["comment_id"],
            "post_id": post_id,
            "content": comment.content,
            "created_by": comment_data["created_by"],
            "created_at": created_at_str
        }
    }

@router.get("/test", response_model=dict)
async def test_endpoint():
    return {"status": "success", "message": "Comment router test endpoint works!"}
