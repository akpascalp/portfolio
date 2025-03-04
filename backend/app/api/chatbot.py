from fastapi import APIRouter
from app.models.chatbot_model import run_mistral

router = APIRouter()

@router.post("/")
async def chatbot(query: str):
    response = run_mistral(query)
    return {"response": response}
