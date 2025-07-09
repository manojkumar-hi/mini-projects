from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from utils import validate_jwt_token
import json

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Define routes that don't need authentication
        self.public_routes = [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/users/signup",
            "/api/v1/users/login"
        ]
    
    async def dispatch(self, request: Request, call_next):
        # Check if the route requires authentication
        if self.is_public_route(request.url.path):
            # Public route, skip authentication
            response = await call_next(request)
            return response
        
        # Protected route, check for authorization
        authorization = request.headers.get("authorization")
        
        if not authorization:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header required"}
            )
        
        # Validate the token
        if not validate_jwt_token(authorization):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"}
            )
        
        # Token is valid, proceed with the request
        response = await call_next(request)
        return response
    
    def is_public_route(self, path: str) -> bool:
        """Check if the route is in the public routes list"""
        return path in self.public_routes
