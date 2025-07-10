from typing import Optional
from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException, Header,File, Form, UploadFile
from models.post import Post
from db import db
from cloudinary_util import upload_file_to_cloudinary
from datetime import datetime
from utils import decode_jwt_token
import json
router = APIRouter()

@router.post("/create", response_model=dict)
async def create_post(
    type: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    tags: Optional[str] = Form(None),  # Comma-separated string
    file: Optional[UploadFile] = File(None),
    Authorization: str = Header(None)
    ):
    user_data = decode_jwt_token(Authorization)
    tags_list = []
    if tags:
        try:
            # Try to parse as JSON first (e.g., ["python", "fastapi", "web"])
            tags_list = json.loads(tags)
        except json.JSONDecodeError:
            # If JSON parsing fails, treat as comma-separated string
            tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    file_url = None   
    if file and file.filename:
        file_url = await upload_file_to_cloudinary(file)
    
    post_data = Post(
        type=type,
        title=title,
        content=content,
        tags=tags_list,
        file_url=file_url,
        post_id=str(uuid4()),  # Generate a unique post ID
        created_by=user_data.get("email"),
        created_at=datetime.now()
    )
    # Insert the post into the database
    result = await db.posts.insert_one(post_data.dict())
    if not result.acknowledged:
        raise HTTPException(
            status_code=500,
            detail="Failed to create post. Please try again later."
        )
    return {
        "status": "success",
        "message": "Post created successfully",
        "data": {
            "id": str(result.inserted_id),
            "type": post_data.type,
            "title": post_data.title,   
            "file_url": file_url,
        }
    }


@router.get("/by-user", response_model=dict)
async def get_all_posts(Authorization: str = Header(None)):
    user_data = decode_jwt_token(Authorization)
    posts = await db.posts.find({"created_by": user_data.get("email")},{"_id":0}).to_list(length=None)
    
    # Convert datetime objects to strings for JSON serialization
    for post in posts:
        if "created_at" in post and post["created_at"]:
            post["created_at"] = post["created_at"].isoformat()
    
    return {
        "status": "success",   
        "data": posts  
    }


@router.get("/", response_model=dict)
async def get_posts():
    posts = await db.posts.find({},{"_id":0}).to_list(length=None)
    
    # Convert datetime objects to strings for JSON serialization
    for post in posts:
        if "created_at" in post and post["created_at"]:
            post["created_at"] = post["created_at"].isoformat()
    
    return {
        "status": "success",   
        "data": posts 
    }

@router.get("/{post_id}/comments", response_model=dict)
async def get_comments(post_id: str):
    try:
        # Simple test - just return empty response first
        return {
            "status": "success",
            "message": f"Testing endpoint for post_id: {post_id}",
            "data": []
        }
    except Exception as e:
        print(f"Error in get_comments: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
