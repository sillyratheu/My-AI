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
    user_prompt = request.prompt.strip()
    user_prompt_lower = user_prompt.lower()
    
    # 1. Owner related fixed reply
    if "owner" in user_prompt_lower or "creator" in user_prompt_lower or "created you" in user_prompt_lower or "who made you" in user_prompt_lower:
        return {"status": "success", "reply": "Ramim is my owner and creator."}

    try:
        # AI ke clear instructions dewa jate she NotRa hoye kotha bole ar OpenAI na bole
        system_msg = "You are NotRa, a helpful AI assistant created by Ramim. Never mention OpenAI."
        full_query = f"{system_msg}\nUser: {user_prompt}\nNotRa:"
        
        ai_url = f"https://text.pollinations.ai/{requests.utils.quote(full_query)}"
        response = requests.get(ai_url, timeout=15)
        
        if response.status_code == 200:
            reply = response.text.strip()
            
            # Jodi ai vul kore openai ba onno kichu bole, seta fix kore dibo
            if "openai" in reply.lower() or "language model" in reply.lower():
                reply = "I am NotRa, created by Ramim. How can I help you?"
                
            if not reply:
                reply = "I am here! What would you like to talk about?"
        else:
            reply = "Let's chat! What's on your mind?"
            
        return {"status": "success", "reply": reply}
        
    except Exception as e:
        # Network ba timeout hole r "I'm NotRa" bar bar ashbe na, normal friendly message dibe
        return {"status": "success", "reply": "Connection is a bit slow, please try sending your message again!"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
    
