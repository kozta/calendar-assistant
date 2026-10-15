from fastapi import FastAPI
from pydantic import BaseModel
from app.assistant import CalendarAssistant
from app.providers.factory import create_llm_provider

from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title="Calendar AI Assistant",
    version="0.2.0",
)

llm_provider = create_llm_provider()

assistant = CalendarAssistant(
    llm_provider=llm_provider
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str



@app.get("/health")
def health():
    return {
        "status": "ok"
    }
    
@app.post(
    "/assistant/chat",
    response_model=ChatResponse,
)

def chat(request: ChatRequest):

    response = assistant.chat(
        message=request.message
    )

    return ChatResponse(
        response=response
    )