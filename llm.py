from pypdf import PdfReader
from dotenv import load_dotenv
import requests
import os



load_dotenv()
ANYTHINGLLM_API_URL = "http://localhost:3001/api/v1"
API_KEY = os.getenv('ANYTHING_LLM_API_KEY') 

    
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Authorization":f'Bearer {API_KEY}'
}


def autenticacao():
    response = requests.get(f"{ANYTHINGLLM_API_URL}/auth", headers=headers)
    try:
        print(response.json())
    except Exception as e:
        print(e)

def todos_workspaces():
    response = requests.get(f'{ANYTHINGLLM_API_URL}/workspaces', headers=headers)
    try:
        print(response.json())
    except Exception as e:
        print(e)

def mensagem_para_o_llm(prompt):
    
    dados = {
    "message":prompt,
    "mode": "query"
    }

    endpoint = f"{ANYTHINGLLM_API_URL}/workspace/legal/chat"
    
    
    response = requests.post(endpoint,json=dados, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"{data.get('textResponse', 'resposta não encontrada')}")     

if __name__ == "__main__":
    prompt = "O que é organização academica?"
    mensagem_para_o_llm(prompt)