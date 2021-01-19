# Dependência para NLP
import spacy
from preprocessing import standardize

# Dependência para rede neural
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

# Outras dependências
import numpy as np
import random
import pickle
import json 
import os

# Definições iniciais
assets_path = os.path.join(os.path.dirname(__file__), 'assets/')  # Diretório de assets
nlp = spacy.load('pt_core_news_md')  # Spacy parser
intents = json.load(open(os.path.join(assets_path, 'data.json'), 'r'))  # Arquivo de dados

# Tratando arquivo de dados
documents = []
vocabulary = []
labels = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        doc = [token.lemma_ for token in nlp(standardize(pattern))]
        tag = intent['tag']
        
        vocabulary.extend(doc)
        labels.append(tag)
        documents.append((doc, tag))

vocabulary = sorted(set(vocabulary))
pickle.dump(vocabulary, open(os.path.join(assets_path, 'vocabulary.pkl'), 'wb'))

labels = sorted(set(labels))
pickle.dump(labels, open(os.path.join(assets_path, 'labels.pkl'), 'wb'))    
        
# Preparando dados para treinamento
training = []
for document in documents:
    word_patterns = document[0]    
    bag = [int(token in word_patterns) for token in vocabulary]

    output = [0] * len(labels)
    output[labels.index(document[1])] = 1

    training.append((bag, output))

random.shuffle(training)
X = np.array([np.array(t[0]) for t in training])
y = np.array([np.array(t[1]) for t in training])

# Treinamento da rede neural
model = Sequential()
model.add(Dense(64, input_shape=(len(X[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
model.summary()

hist = model.fit(X, y, epochs=200, batch_size=5, verbose=True)
model.save(os.path.join(assets_path, 'chatbot.h5'), hist)
