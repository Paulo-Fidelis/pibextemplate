from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import requests
import os

#Pré configurações
load_dotenv()
ANYTHINGLLM_API_URL = "http://localhost:3001/api/v1"
API_KEY = os.getenv('ANYTHING_LLM_API_KEY') 
    
headers = {
    "accept": "application/json",
    "Authorization":f'Bearer {API_KEY}'
}

# Criação da API

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/llmResponse/{prompt}')
def hello(prompt):
    dados = {
    "message":prompt,
    "mode": "query"
    }

    endpoint = f"{ANYTHINGLLM_API_URL}/workspace/legal/chat"
    response = requests.post(endpoint,json=dados, headers=headers)
    
    try:  
      data = response.json()
      resposta = data.get('textResponse')
      return {"response": resposta}
    except Exception as e:
       print(e)
       return None
    

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_content = await file.read()

    endpoint = f"{ANYTHINGLLM_API_URL}/document/upload"

    data = {
        "addToWorkspaces": "legal"
    }

    files = {
        "file": (file.filename, file_content, file.content_type)
    }
    try:
        response = requests.post(endpoint, files=files, data=data, headers=headers)
        return response.json()

    except Exception as e:
        print(e)
       