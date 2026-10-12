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
    
    # Shudhumatro owner jigges korle ei fixed answer ta dibe, baki shob question AI solve korbe
    if any(k in user_prompt_lower for k in ["owner", "creator", "created you", "who made you"]):
        return {"status": "success", "reply": "Ramim is my owner and creator! He built me."}

    try:
        # NotRa identity set kore direct AI er kach thekei real answer ante hobe
        system_instruction = "You are NotRa, a helpful AI best friend created by Ramim. Give accurate, detailed answers to any question asked by the user. Never mention OpenAI."
        full_query = f"{system_instruction}\nUser: {user_prompt}\nNotRa:"
        
        ai_url = f"https://text.pollinations.ai/{requests.utils.quote(full_query)}"
        
        # Timeout 45 seconds kore dewa holo jate deri holeo AI answer generate kore dite pare
        response = requests.get(ai_url, timeout=45)
        
        if response.status_code == 200:
            reply = response.text.strip()
            
            # Jodi AI vul kore openai bole, seta override kore dibo
            if "openai" in reply.lower() or "language model" in reply.lower():
                reply = reply.replace("OpenAI", "Ramim").replace("open-ai", "Ramim")
                
            # Jodi kono karone empty ashe, tobe abar try korar kotha bolbe
            if not reply:
                reply = "Ektu deri hocche, kintu ami chesta korchi tomar question-er proper answer dite. Abar try koro!"
        else:
            reply = "Server ektu busy, kintu ami answer khujchi. Ektu pore abar pathao!"
            
        return {"status": "success", "reply": reply}
        
    except Exception as e:
        return {"status": "success", "reply": "Connection slow thakay answer aste ektu time lagche, kintu ami answer debo!"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
