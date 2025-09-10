from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import requests
import os


load_dotenv()
ANYTHINGLLM_API_URL = "http://localhost:3001/api/v1"
API_KEY = os.getenv('ANYTHING_LLM_API_KEY') 

recognizer = sr.Recognizer()
engine = pyttsx3.init()

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


'''@app.get('/llmlisten/')
def escutar():
 with sr.Microphone() as microfone:       
    try:
        fala = recognizer.listen(microfone)
        texto = recognizer.recognize_google(fala, language="pt-BR") #A biblioteca usa uma API do Google
        print(f"Você disse: {texto}")
        return texto
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        return None
    except sr.RequestError as e:
        print(f"Erro no serviço de reconhecimento de fala: {e}")
        return None
'''

'''
@app.get('/llmSay/{response}')
def falar(response):
    engine.say(response)
    engine.runAndWait()
'''
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
       