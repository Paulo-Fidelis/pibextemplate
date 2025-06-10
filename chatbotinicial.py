import re
import random

respostas = {
    r"oi|olá|e aí|eae|eai|opa": ["Olá", "Oi", "E aí, tudo bem?", "Opa, tudo certo?"],
    r"como você está\??|você está bem\??|como tem estado\??": ["Estou bem, e você?", "Tenho estado bem, obrigado", "Tudo certo, e com você?"],
    r"como é o seu nome\??|como você se chama\??|quem é você\??": ["Meu nome é Pyman, muito prazer.", "Eu sou o Pyman, prazer em conhecer!"],
    r"o que você faz\??|qual a sua função\??": ["Eu ajudo os usuários a entenderem melhor a plataforma e como utilizá-la da maneira que lhes for útil", "Minha função é te ajudar a navegar pela plataforma da melhor maneira", "Eestou aqui para te ajudar a utlizar a plataforma, qual a sua dúvida?"],
    r"tchau|até mais|até a próxima|adeus|até logo|falou": ["Tchau, foi um prazer ajudar!", "Até mais, quando precisar estou aqui!", "Até logo, foi bom falar com você."]
}
def responder(mensagem_usuario):
    mensagem_usuario = mensagem_usuario.lower()

    for regulares, respostas_possiveis in respostas.items():
        if re.search(regulares, mensagem_usuario):
            return random.choice(respostas_possiveis)
           

    return "Não entendi, pode repetir ou reformular a pergunta?"

print("Chatbot Pyman\n")
print("Para encerrar a conversa, digite 'sair'\n")

while True:
    entrada = input("Digite a entrada inicial")

    if entrada is None:
        continue 
   
    if entrada.lower() == 'sair':
        print("Pyman: Até a próxima!")
        break

    resposta = responder(entrada)
    print(f"Pyman: {resposta}")
  