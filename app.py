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
    
    # Owner related fixed reply
    if "owner" in user_prompt_lower or "creator" in user_prompt_lower or "created you" in user_prompt_lower or "who made you" in user_prompt_lower:
        return {"status": "success", "reply": "Ramim is my owner and creator."}

    try:
        # Ebar aro ekta fast ar stable free public model use kora hocche
        api_url = f"https://text.pollinations.ai/{requests.utils.quote(user_prompt)}"
        response = requests.get(api_url, timeout=20)
        
        if response.status_code == 200:
            reply = response.text.strip()
            
            # Jodi ai vul kore openai ba onno kichu bole
            if "openai" in reply.lower() or "language model" in reply.lower():
                reply = "I am NotRa, created by Ramim. How can I help you?"
                
            # Jodi khali reply ashe tahole user-er prompt er upor base kore ekta smart reply dibe, r "Let's chat" bolbe na
            if not reply or len(reply) < 2:
                reply = f"That's an interesting question about '{user_prompt}'. As NotRa, created by Ramim, I am always learning to answer better!"
        else:
            reply = f"I am NotRa, built by Ramim. You asked about: {user_prompt}."
            
        return {"status": "success", "reply": reply}
        
    except Exception as e:
        return {"status": "success", "reply": f"As NotRa, created by Ramim, I am here to help you with: {user_prompt}"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
    
