from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException, Header
from models.user import User, UserLogin
from db import db
from utils import get_hashed_password, check_password, validate_jwt_token, create_jwt_token
from typing import Optional
import jwt

router = APIRouter()

@router.post("/signup", response_model=dict)
async def create_user(user: User):
    # Check if user already exists by email
    user_exists = await db.users.count_documents({"email": user.email}) > 0
    if user_exists:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Insert new user
    user.password = get_hashed_password(user.password)
    user.user_id=str(uuid4()) # Generate a unique user ID
    result = await db.users.insert_one(user.dict())

    print(f"User created with id: {result.inserted_id}")

    return {
        "status": "success",
        "message": "User created successfully",
        "data":{
            "id": str(result.inserted_id),
            "name": user.name,
            "email": user.email,
        }
    }

@router.post("/login", response_model=dict)
async def login_user(payload: UserLogin):
    print(f"Login attempt for email: {payload.email}")
    user = await db.users.find_one({"email": payload.email})
    if not user:
        print("User not found!")
        raise HTTPException(status_code=404, detail="User not found")
    
    print("User found, checking password...")
    if not check_password(user['password'], payload.password):
        print("Password check failed!")
        raise HTTPException(status_code=401, detail="Invalid password")
    
    print("Password check passed, creating token...")
    
    # Test if create_jwt_token function exists and works
    print("Testing token creation...")
    try:
        test_data = {"email": user['email']}
        print(f"Input data: {test_data}")
        token = create_jwt_token(test_data)
        print(f"Generated token: {token}")
        print(f"Token type: {type(token)}")
    except Exception as e:
        print(f"ERROR creating token: {e}")
        import traceback
        traceback.print_exc()
        token = "ERROR"
    
    return {
        "status": "success",
        "message": "Login successful",
        "data": {
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email'],
            "token": token
        }
    }

@router.get("/", response_model=dict) 
async def get_users():
    
    users = await db.users.find({},{"_id":0}).to_list(length=100)
    return {
        "status": "success",
        "message": "Users retrieved successfully",
        "data": users
    }





