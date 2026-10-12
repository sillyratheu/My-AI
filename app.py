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
    
    # Kew owner ba creator niye jigges korle ei fixed answer dibe
    if "owner" in user_prompt_lower or "creator" in user_prompt_lower or "created you" in user_prompt_lower or "who made you" in user_prompt_lower:
        return {"status": "success", "reply": "Ramim is my owner and creator."}

    try:
        ai_url = f"https://text.pollinations.ai/{requests.utils.quote(user_prompt)}"
        response = requests.get(ai_url, timeout=10)
        
        if response.status_code == 200:
            reply = response.text.strip()
            
            # Jodi ai bole openai ba onno kichu, seta override kore dibo
            if "openai" in reply.lower() or "language model" in reply.lower():
                reply = "I'm NotRa, what's on your mind today?"
                
            if not reply:
                reply = "I'm NotRa, what's on your mind today?"
        else:
            reply = "I'm NotRa, what's on your mind today?"
            
        return {"status": "success", "reply": reply}
        
    except Exception as e:
        return {"status": "success", "reply": "I'm NotRa, what's on your mind today?"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
    
