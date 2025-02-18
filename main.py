from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import subprocess


app = FastAPI()

class Prompt(BaseModel):
    prompt: str

def run_ollama(prompt: str):
    result = subprocess.run(['ollama', 'run', 'llama3.2:3B', prompt], capture_output=True, text=True)
    return ''.join(c for c in result.stdout if c.isprintable())



@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/api/llama")
async def llama_api(prompt: Prompt):
    # Appel asynchrone de la fonction d'exécution
    response = run_ollama(prompt.prompt)
    return {"response": response}
