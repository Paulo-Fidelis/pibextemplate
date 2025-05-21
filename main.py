from fastapi import FastAPI
from dotenv import load_dotenv
import requests
import os

#Pré configurações
load_dotenv()
ANYTHINGLLM_API_URL = "http://localhost:3001/api/v1"
API_KEY = os.getenv('ANYTHING_LLM_API_KEY') 
    
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Authorization":f'Bearer {API_KEY}'
}


# Criação da API

app = FastAPI()

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
    
 