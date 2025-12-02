from fastapi import FastAPI
from pydantic import BaseModel
from .services.rag import get_rag_response

app = FastAPI()

class ChatMessage(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "FastAPI backend is running!"}

@app.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
    response = await get_rag_response(chat_message.message)
    return {"response": response}