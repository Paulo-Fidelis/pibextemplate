from together import Together
from pypdf import PdfReader
from dotenv import load_dotenv

caminho = "./pdfs/organizacaoacademica_atualizada_marco_2016.pdf"

leitor = PdfReader(caminho)

client = Together()

perguntas = []
respostas = []

text = ""
for page in leitor.pages:
    text += page.extract_text() + "\n"

load_dotenv()

prompt = f'''Crie várioas perguntas e respostas que resumam o documento que estou lhe passando:{text}.
             As perguntas devem seguir o formato a seguir: 
             
             Pergunta 1: pergunta criada;
             Resposta 1: resposta da pergunta acima;

             A resposta deve ter apenas as perguntas e respostas e você deve pôr o ponto e vírgula ao final de todas as respostas criadas.
    '''
promptTeste = f"a reposta que você me traz está em que formato de dado?"



response = client.chat.completions.create(
    model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
    messages=[{"role": "user", "content":prompt}],
  )

# print(response.choices[0].message.content)
    

resposta_string = str(response.choices[0].message.content)

print(resposta_string.split("; "))

for dupla in resposta_string:
  perguntas.append(dupla[0])      
  respostas.append(dupla[1])

print(perguntas)
print(respostas)