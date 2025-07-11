import uvicorn
from fastapi import FastAPI
from routes.comment_router import router as comment_router
from routes.user_router import router as user_router
from middleware import AuthMiddleware
from routes.post_router import router as post_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="StudentHub API", version="1.0.0")

# CORS middleware MUST come FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# AuthMiddleware comes AFTER CORS
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(post_router, prefix="/api/v1/posts", tags=["posts"])
app.include_router(comment_router, prefix="/api/v1/comments", tags=["comments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to StudentHub API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
