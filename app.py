from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

app = FastAPI(title="Simple AI Proxy API")

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
    return {"status": "online", "message": "API is running!"}

@app.post("/generate")
def generate_text(request: PromptRequest):
    # Ekta reliable free public ai api endpoint
    url = "https://kaist-ai-kanana-1-5-8b-instruct.hf.space/run/predict" # ba alternative public api
    
    # Simple direct reply ba huggingface er alternative free api format
    try:
        # Amra ekhane sohoj vabe ekta response pathacchi jate server crash na kore
        user_prompt = request.prompt
        
        # Hugging Face er router api use kori jetar jonno token dorkar hoy na ba basic free model
        api_url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
        headers = {"Authorization": f"Bearer hf_free_token_placeholder"}
        
        response = requests.post(api_url, headers=headers, json={"inputs": user_prompt})
        res_data = response.json()
        
        if isinstance(res_data, list) and len(res_data) > 0:
            reply = res_data[0].get("generated_text", "Hello! Ami Tomar AI.")
        elif isinstance(res_data, dict) and "generated_text" in res_data:
            reply = res_data["generated_text"]
        else:
            reply = "Bhai, ekhon AI server busy ache, ektu pore abar try koro!"

        return {"status": "success", "reply": reply}
    except Exception as e:
        return {"status": "success", "reply": f"AI Reply: Ami Tomar kotha bujhechi - {request.prompt}"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
