from fastapi import APIRouter
from pydantic import BaseModel
from app.model import ChatModel

router = APIRouter()
model = ChatModel("data/training.csv")

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    return {"reply": model.predict(req.message)}
