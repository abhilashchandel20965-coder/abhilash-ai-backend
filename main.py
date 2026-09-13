import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Abhilash AI JARVIS")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not configured")

client = OpenAI(api_key=api_key)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "assistant": "Abhilash AI JARVIS"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=(
                "तुम Abhilash AI JARVIS हो। "
                "उपयोगकर्ता से मुख्यतः शुद्ध हिंदी देवनागरी में बात करो। "
                "उत्तर स्पष्ट, उपयोगी और सुरक्षित रखो। "
                "किसी बाहरी या महत्वपूर्ण कार्रवाई को उपयोगकर्ता की स्पष्ट अनुमति "
                "के बिना स्वयं न करो।"
            ),
            input=request.message
        )

        return {
            "reply": response.output_text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="AI service error"
        )
