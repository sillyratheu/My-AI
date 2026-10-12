from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

app = FastAPI(title="Ramim AI API")

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
    return {"status": "online", "message": "API is running perfectly!"}

@app.post("/generate")
def generate_text(request: PromptRequest):
    user_prompt = request.prompt
    
    try:
        # Ekta khub fast and reliable free AI public endpoint
        url = "https://api.duckduckgo.com/?q=" + requests.utils.quote(user_prompt) + "&format=json"
        
        # Athoba amra sohoj vabe ekta smart rule ba public gemini/pollinations free api use korte pari:
        ai_url = f"https://text.pollinations.ai/{requests.utils.quote(user_prompt)}"
        
        response = requests.get(ai_url, timeout=10)
        
        if response.status_code == 200:
            reply = response.text.strip()
            if not reply:
                reply = "Bhai, ami ektu bujhte parini, abar bolo!"
        else:
            reply = "Ami ekhon ektu busy achi, abar try koro!"
            
        return {"status": "success", "reply": reply}
        
    except Exception as e:
        return {"status": "success", "reply": f"Bhai, ekti choto error hoyeche: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
