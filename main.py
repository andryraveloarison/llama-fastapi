from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import subprocess
import re

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

def remove_ansi_escape_sequences(text: str) -> str:
    ansi_escape = re.compile(r'\x1b\[[0-9;]*[mGKF]')
    return ansi_escape.sub('', text)

async def run_ollama(prompt: str):
    try:
        process = await asyncio.create_subprocess_exec(
            'ollama', 'run', 'llama3.2:3B', prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=120)

        decoded_stdout = stdout.decode('utf-8')
        decoded_stderr = stderr.decode('utf-8')

        # Expression régulière pour supprimer les séquences ANSI
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        cleaned_stderr = ansi_escape.sub('', decoded_stderr)

        return decoded_stdout

    except asyncio.TimeoutError:
        return "Error: Timeout reached while waiting for Ollama response."
    except Exception as e:
        return f"Failed to run Ollama: {str(e)}"

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/api/llama")
async def llama_api(prompt: Prompt):
    # Appel asynchrone de la fonction d'exécution
    response = await run_ollama(prompt.prompt)
    return {"response": response}
