from fastapi import APIRouter
from pydantic import BaseModel
from app.models.chatbot_model import run_mistral

router = APIRouter()

class ChatbotQuery(BaseModel):
    user_input: str

@router.post("/")
async def chatbot(query: ChatbotQuery):
    response = run_mistral(query.user_input)
    return {"response": response}
