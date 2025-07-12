from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from utils import validate_jwt_token

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
            "/api/v1/users/login",
             "/api/v1/posts" ,
            "/api/v1/posts/" 
        ]
    
    async def dispatch(self, request: Request, call_next):
        print(f"Middleware called for path: {request.url.path}")

        # Allow all OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            print("OPTIONS request detected, skipping auth.")
            return await call_next(request)

        # Check if the route requires authentication
        if self.is_public_route(request.url.path):
            print(f"Public route detected: {request.url.path}")
            # Public route, skip authentication
            response = await call_next(request)
            return response
        
        print(f"Protected route detected: {request.url.path}")
        
        # Protected route, check for authorization
        authorization = request.headers.get("authorization")
        print(f"Authorization header: {authorization}")
        
        if not authorization:
            print("No authorization header found")
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header required"}
            )
        
        # Validate the token
        print(f"About to validate token: {authorization[:50]}..." if len(authorization) > 50 else f"About to validate token: {authorization}")
        
        try:
            token_valid = validate_jwt_token(authorization)
            print(f"Token validation result: {token_valid}")
        except Exception as e:
            print(f"Error during token validation: {e}")
            token_valid = False
        
        if not token_valid:
            print("Token validation failed - returning 401")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"}
            )
        
        print("Token is valid, proceeding to route")
        # Token is valid, proceed with the request
        response = await call_next(request)
        return response
    
    def is_public_route(self, path: str) -> bool:
        """Check if the route is in the public routes list"""
        return path in self.public_routes
