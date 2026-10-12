from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

app = FastAPI(title="NotRa AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "online", "message": "NotRa API is running perfectly!"}

@app.post("/generate")
def generate_text(request: PromptRequest):
    user_prompt = request.prompt
    
    try:
        # সিস্টেম প্রম্পটে পরিষ্কার বলে দেওয়া হলো যে এর নাম NotRa এবং এর মালিক Ramim
        system_instruction = "You are NotRa, an advanced AI assistant. Your creator and owner is Ramim. Never say you are created by OpenAI. Answer cleanly and accurately."
        full_prompt = f"{system_instruction}\nUser: {user_prompt}\nNotRa:"
        
        ai_url = f"https://text.pollinations.ai/{requests.utils.quote(full_prompt)}"
        
        response = requests.get(ai_url, timeout=30)
        
        if response.status_code == 200:
            reply = response.text.strip()
            if not reply:
                reply = "Hello! Please try sending your message again."
        else:
            reply = "Servers are busy right now, please try again later!"
            
        return {"status": "success", "reply": reply}
        
    except Exception as e:
        return {"status": "success", "reply": "Network connection error, please try again!"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
