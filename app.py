from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI(title="Render Free LLM API")

# একটি হালকা ও ফাস্ট মডেল লোড করা (CPU-র জন্য অপ্টিমাইজড)
MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

print("Loading model... Please wait...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, 
    torch_dtype=torch.float32, 
    low_cpu_mem_usage=True
)
print("Model loaded successfully!")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_text(request: PromptRequest):
    try:
        inputs = tokenizer(request.prompt, return_tensors="pt")
        
        # জেনারেট করার প্যারামিটার
        outputs = model.generate(
            **inputs, 
            max_new_tokens=150, 
            temperature=0.7, 
            do_sample=True
        )
        
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"status": "success", "reply": response_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
