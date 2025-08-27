from fastapi import FastAPI
from app.routers import game, user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="guessthestock-frontend/build/static"), name="static")
@app.get("/")
async def root():
    return FileResponse("guessthestock-frontend/build/index.html")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000","http://localhost:8001","http://localhost:3000","http://localhost:3001"
                   "https://www.michael-mak.ca/",'https://www.michael-mak.com/'],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],  # or restrict to ["GET", "POST"]
    allow_headers=["*"],
)


app.include_router(game.router, prefix="/game", tags=["Game"])
#app.include_router(user.router, prefix="/user", tags=["User"])