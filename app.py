from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, MetaData, LargeBinary, select
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv 
from together import Together
from pypdf import PdfReader
import io
from flask import *
import os

load_dotenv()

db_file = 'sqlite:///C:/Users/paulo/Pibex/docs.db'

client = Together()


app = Flask(__name__)
Base = declarative_base()

engine = create_engine(db_file, echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


class Document(Base):
  __tablename__ = 'Documents'

  id = Column(Integer, primary_key=True)
  nome_document = Column(String, nullable=False)
  document = Column(LargeBinary, nullable=False)

  pergunta = relationship("Pergunta", back_populates="document")


class Resposta(Base):
  __tablename__ = "Respostas"

  id = Column(Integer, primary_key=True)
  resposta = Column(String, nullable=False)

  pergunta = relationship("Pergunta", back_populates="respostas")

class Pergunta(Base):
  __tablename__ = "Perguntas"

  id = Column(Integer, primary_key=True)
  pergunta = Column(String, nullable=False)
  id_document = Column(Integer, ForeignKey('Documents.id'))
  id_resposta = Column(Integer, ForeignKey('Respostas.id'))

  document = relationship("Document", back_populates="pergunta")
  respostas = relationship("Resposta", back_populates="pergunta")


def Insert_resposta(resposta):
  with Session(engine) as session:
    nova_resposta = Resposta(
      resposta=resposta
    )
    try:
      session.add(nova_resposta)
    except Exception as e:
      session.rollback()
      print(e)
      return None
    finally:
      session.commit()
      return 'foi mano'
    

def Insert_document(file):
  with Session(engine) as session:
    arquivo_pdf = file.read()
    nome = os.path.basename(file)

    novo_documento = Document(
      nome_document = nome,
      document = arquivo_pdf
    )
    
    try:
      session.add(novo_documento)
    except Exception as e:
      session.rollback()
      print(e)
      return None
    finally:
      session.commit()
      return 'foi mano'


def Insert_pergunta(pergunta, nome_documento, resposta):
  with Session(engine) as session:
    query_document = select(Document.id).where(nome_document=nome_documento)
    query_resposta = select(Resposta.id).where(resposta=resposta)
    nova_pergunta = Pergunta(
      pergunta=pergunta,
      id_document = query_document,
      id_resposta = query_resposta
    )
    try: 
      session.add(nova_pergunta)
    except Exception as e:
      session.rollback()
      print(e)
      return None
    finally:
      session.commit()
      return 'foi mano'


@app.route('/')
def home():

  with Session() as session:
    query_all_documents = session.query(Document).all()
    for document in query_all_documents:
      document.extracao_texto = ''

      pdf = getattr(document, 'document', None)
      pdf_file = io.BytesIO(pdf)
      pdf_reader = PdfReader(pdf_file)

      primeira_pagina = pdf_reader.pages[0].extract_text()

      document.extracao_texto = primeira_pagina
      
  return render_template('index.html', documents=query_all_documents)

@app.route('/inserirDocument', methods=['POST'])
def insertDocument():
  nome = request.form['NomeDocument']
  arquivo = request.files['fileDocument']
  pdf_reader = PdfReader(arquivo)

  text = ""
  for page in pdf_reader.pages:
    text += page.extract_text() + "\n"

  prompt = f'''Crie várioas perguntas e respostas que resumam o documento que estou lhe passando:{text}.
             As perguntas devem seguir o formato a seguir: 
             
             Pergunta 1: *pergunta criada*
             Resposta 1: *resposta da pergunta acima*

             A resposta deve ter apenas as perguntas e respostas.
    '''

  response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages=[{"role": "user", "content":prompt}],
  )

  pdf_bytes = arquivo.read()1
  
  with Session() as session:
    novo_document = Document(
      nome_document = nome,
      document = pdf_bytes
    )

    try:
      session.add(novo_document)
    except Exception as e:
      session.rollback()
      print(e)
      return None
    finally:
      session.commit()
      return redirect('/')

#Cloud IA usando o framework Together
client = Together()


stream = client.chat.completions.create(
  model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
  messages=[{"role": "user", "content": "What are the top 3 things to do in New York?"}],
  stream=True,
)

for chunk in stream:
  print(chunk.choices[0].delta.content or "", end="", flush=True)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)