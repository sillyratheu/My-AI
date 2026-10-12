from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import uvicorn

app = FastAPI(title="Lightweight Hugging Face Proxy API")

# CORS Middleware যুক্ত করা
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
HF_TOKEN = os.getenv("HF_TOKEN", "hf_free_token_placeholder")

class PromptRequest(BaseModel):
    prompt: str

# ১. হোম পেজ রুট (যাতে মূল লিঙ্কে ঢুকলে 404 না আসে)
@app.get("/")
def home():
    return {"status": "online", "message": "AI API is running successfully! Use /generate endpoint with POST method."}

# ২. জেনারেট রুট
@app.post("/generate")
def generate_text(request: PromptRequest):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": request.prompt,
        "parameters": {"max_new_tokens": 250, "return_full_text": False}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            reply = result[0].get("generated_text", "No response generated")
        elif isinstance(result, dict) and "error" in result:
            reply = f"API Error: {result['error']}"
        else:
            reply = str(result)
            
        return {"status": "success", "reply": reply}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
