import json
import os 
import pickle
import nltk
import random
import numpy as np

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

#nltk.download('punkt')
#nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

training = []
palavras = []
documentos = []
intencoes = json.loads(open('intents.json').read())

classes = [i['tag'] for i in intencoes['intents']]

ignore_palavras = ["!", "@", "#", "$", "%", "*", "?"]

for intencao in intencoes['intents']:
  for padrao in intencao['patterns']:
    palavra = nltk.word_tokenize(padrao)
    palavras.extend(palavra)
    documentos.append((palavra, intencao['tag']))

palavras = [lemmatizer.lemmatize(p.lower()) for p in palavras if p not in ignore_palavras]

palavras = sorted(list(set(palavras)))
classes = sorted(list(set(classes)))

pickle.dump(palavras, open('palavras.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

output_empty = [0] * len(classes)
for documento in documentos: 
    bolsa = []
    padrao_palavras = documento[0]

    padrao_palavras = [lemmatizer.lemmatize(palavra.lower()) for palavra in padrao_palavras]

    for palavra in palavras:
       bolsa.append(1) if palavra in padrao_palavras else bolsa.append(0)

    output_row = list(output_empty)
    output_row[classes.index(documento[1])] = 1

    training.append([bolsa, output_row])

random.shuffle(training)
training = np.array(training)

x = list(training[:, 0])
y = list(training[:, 1])


model = Sequential()
model.add(Dense(128, input_shape=(len(x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',optimizer=sgd, metrics=['accuracy'])

m = model.fit(np.array(x), np.array(y), epochs=200, batch_size=5, verbose=1)