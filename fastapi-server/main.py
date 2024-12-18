from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
import tempfile

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"], 
    allow_headers=["*"], 
)

@app.get("/")
async def root():
    return {"message": "CORS is working!"}

class CodeExecutionRequest(BaseModel):
    code: str

@app.post("/execute/{language}")
async def execute_code(language: str, request: CodeExecutionRequest):
    if language == "python":
        return execute_python(request.code)
    elif language == "javascript":
        return execute_javascript(request.code)
    elif language == "php":
        return execute_php(request.code)
    else:
        raise HTTPException(status_code=400, detail="Unsupported language")

def execute_python(code: str):
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w', encoding='utf-8') as tmp_file:
        tmp_file.write(code)
        tmp_file_name = tmp_file.name
       
    try:
        result = subprocess.run(["python", tmp_file_name], capture_output=True, text=True, encoding='utf-8')
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    finally:
        os.remove(tmp_file_name)

def execute_javascript(code: str):
    with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode='w', encoding='utf-8') as tmp_file:
        tmp_file.write(code)
        tmp_file_name = tmp_file.name
       
    try:
        result = subprocess.run(["node", tmp_file_name], capture_output=True, text=True, encoding='utf-8')
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    finally:
        os.remove(tmp_file_name)

def execute_php(code: str):
    with tempfile.NamedTemporaryFile(suffix=".php", delete=False,  mode='w', encoding='utf-8') as tmp_file:
        tmp_file.write(code)
        tmp_file_name = tmp_file.name

    try:
        result = subprocess.run(["php", tmp_file_name], capture_output=True, text=True, encoding='utf-8')
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        os.remove(tmp_file_name)