from fastapi import FastAPI
from app.routers import game, user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],  # or restrict to ["GET", "POST"]
    allow_headers=["*"],
)


app.include_router(game.router, prefix="/game", tags=["Game"])
#app.include_router(user.router, prefix="/user", tags=["User"])