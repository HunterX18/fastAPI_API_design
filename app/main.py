from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# from .db.init_db import init_db

from app.routers.post import PostRouter
from app.routers.user import UserRouter
from app.routers.auth import AuthRouter
from app.routers.vote import VoteRouter

# init_db()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

@app.get("/")
def index():
    return { "message": "Hello World!" }

app.include_router(AuthRouter)
app.include_router(PostRouter)
app.include_router(UserRouter)
app.include_router(VoteRouter)
