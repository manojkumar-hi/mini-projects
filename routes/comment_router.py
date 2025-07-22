from datetime import datetime
import token
from fastapi import APIRouter, HTTPException,Request,Header
from models.comment import Comment
from db import db
import jwt
from bson import ObjectId
from utils import decode_jwt_token
from uuid import uuid4



router = APIRouter()

@router.post("/posts/{post_id}/comments", response_model=dict)
async def create_comment(
    post_id: str,
    comment: Comment,
    Authorization: str = Header(None)
):
    post_exists = await db.posts.count_documents({"post_id": post_id}) > 0
    if not post_exists:
        raise HTTPException(status_code=404, detail="Post not found")
    
    user_data = decode_jwt_token(Authorization)

    
    comment_data=comment.dict()
    comment_data['comment_id']= str(uuid4())
    comment_data['created_at'] =  datetime.utcnow()
    comment_data['created_by'] = user_data.get('email')
    
    result = await db.comments.insert_one(comment_data)
    if not result.acknowledged:
        raise HTTPException(
            status_code=500,
            detail="Failed to create comment. Please try again later."
        )
    return{
            "status": "success",
            "message": "Comment created successfully",
            "data": {
                "id": str(result.inserted_id),
                "post_id": comment.post_id,
                "content": comment.content,
                "created_by": comment_data['created_by'],
                "created_at": comment_data['created_at']
            }
        }
