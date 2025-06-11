import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt_tab')
nltk.download('rslp')

pares = [
    ("oi|olá|e aí", ["Olá!", "Oi!", "Como posso ajudar?"]),
    ("qual é o seu nome?", ["Meu nome é BotNLTK.", "Pode me chamar de BotNLTK."]),
    ("como você está?", ["Estou bem, obrigado!", "Tudo certo!"]),
    ("tchau|até mais", ["Até logo!", "Tchau!"]),
]

perguntas = []
indice_respostas = [] 

for idx, (padrao, respostas_lista) in enumerate(pares):
    perguntas_split = padrao.split("|")
    perguntas.extend(perguntas_split)
    indice_respostas.extend([idx] * len(perguntas_split))

respostas = [resposta for _, resposta in pares]

def tokenizacao(texto):
    return nltk.word_tokenize(texto.lower(), language='portuguese')

def stemetizacao(palavras):
    stemmer = nltk.stem.RSLPStemmer()
    return [stemmer.stem(palavra) for palavra in palavras]

def processamento_textual(texto):
    return stemetizacao(tokenizacao(texto))

vectorizer = TfidfVectorizer(tokenizer=processamento_textual, analyzer='word')
tfidf = vectorizer.fit_transform(perguntas)

def responder(pergunta_usuario):
    pergunta_tfidf = vectorizer.transform([pergunta_usuario])

    similaridades = cosine_similarity(pergunta_tfidf, tfidf)

    indice_pergunta = similaridades.argmax()
    
    if similaridades[0][indice_pergunta] > 0.1:
        indice_resposta = indice_respostas[indice_pergunta]
        return random.choice(respostas[indice_resposta])
    else:
        return "Desculpe, não entendi. Pode reformular?"


print("BotNLTK: Olá! Como posso ajudar? (Digite 'tchau' para sair)")

while True:
    entrada = input("Você: ").lower()
    
    if entrada in ["tchau", "até mais", "adeus"]:
        print("BotNLTK: Até logo!")
        break
    
    resposta = responder(entrada)
    print("BotNLTK:", resposta)