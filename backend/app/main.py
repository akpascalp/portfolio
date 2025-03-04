from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api import recognition, sir, chatbot

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recognition.router, prefix="/recognition", tags=["recognition"])
app.include_router(sir.router, prefix="/sir", tags=["sir"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
