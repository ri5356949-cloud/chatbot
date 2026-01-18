from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="SmartSupport AI")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/")
def health_check():
    return {"status": "Backend is running"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful customer support assistant."},
                {"role": "user", "content": req.message}
            ]
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"AI Error: {e}"

    return {"reply": reply}
