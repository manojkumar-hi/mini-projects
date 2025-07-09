from uuid import uuid4 
from fastapi import APIRouter, HTTPException, Header
from models.comment import Comment
from db import db
from typing import Optional
import jwt
from bson import ObjectId
from utils import decode_jwt_token
from datetime import datetime
router = APIRouter()

@router.post("/create", response_model=dict)
async def create_user(comment: Comment,Authorization: Optional[str] = Header(None)):
    posts_exists= await db.posts.count_documents({"post_id":comment.post_id}) > 0
    if not posts_exists:
        raise HTTPException(status_code=404, detail="Post not found")
    
    user_data = decode_jwt_token(Authorization)

    comment_data = comment.dict()
    comment_data["comment_id"] = str(uuid4()) # Generate a unique comment ID
    comment_data["created_at"] = datetime.now() 
    comment_data["created_by"] = user_data.get("email")  
    result = await db.comments.insert_one(comment_data)
    if not result.acknowledged:
        raise HTTPException(
            status_code=500,
            detail="Failed to create comment. Please try again later."
        )
    return {
        "status": "success",
        "message": "Comment created successfully",
        "data": {
            "id": str(result.inserted_id),
            "post_id": comment.post_id,
            "content": comment.content,
            "created_by": comment_data["created_by"],
            "created_at": comment_data["created_at"]
        }
    }
    # # Check if user already exists by email
    # user_exists = await db.users.count_documents({"email": user.email}) > 0
    # if user_exists:
    #     raise HTTPException(status_code=400, detail="User with this email already exists")

    # # Insert new user
    # user.password = get_hashed_password(user.password)
    # result = await db.users.insert_one(user.dict())

    # print(f"User created with id: {result.inserted_id}")

    # return {
    #     "status": "success",
    #     "message": "User created successfully",
    #     "data":{
    #         "id": str(result.inserted_id),
    #         "name": user.name,
    #         "email": user.email,
    #     }
    # }