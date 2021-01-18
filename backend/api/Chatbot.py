# Flask framework
from flask_restful import Resource, reqparse
from flask import jsonify

# Outras dependências
import numpy as np
import random
import pickle
import json
import os

import spacy
from .preprocessing import standardize

from tensorflow.keras.models import load_model


# Definições iniciais
assets_path = os.path.join(os.path.dirname(__file__), 'assets/')  # Diretório de assets
nlp = spacy.load('en_core_web_md')  # Spacy parser
intents = json.load(open(os.path.join(assets_path, 'data.json'), 'r'))  # Arquivo de dados
vocabulary = pickle.load(open(os.path.join(assets_path, 'vocabulary.pkl'), 'rb'))  # Palavras do vocabulário
labels = pickle.load(open(os.path.join(assets_path, 'labels.pkl'), 'rb'))  # Intenções / tipo de perguntas
model = load_model(os.path.join(assets_path, 'chatbot.h5'))  # Carregando rede neural


# Classe do chatbot
class Chatbot(Resource):
    
    def __init__(self):
        pass

    def get(self):
        response = jsonify({'message': 'Requisição deve ser do tipo POST'})
        response.status_code = 400
        return response

    def post(self):
        # Identificar argumento 'message'
        parser = reqparse.RequestParser()
        parser.add_argument('message', required=True, location='json')
        args = parser.parse_args()
        message = args['message'].strip()

        # Predict da resposta
        ints = self.predict(message, labels, vocabulary, nlp)
        res = self.get_response(ints)

        # Formular reponsta
        response = jsonify({'message': res})
        response.status_code = 200
        return response

    def lemma_tokenization(self, sentence:str, nlp):
        clean_sentence = standardize(sentence)
        tokens = [token.lemma_ for token in nlp(clean_sentence)]

        return tokens

    def bag_of_words(self, sentence:str, vocabulary:list, nlp):
        tokens = self.lemma_tokenization(sentence, nlp)
        bag = [int(tk in tokens) for tk in vocabulary]
        
        return np.array(bag)    

    def predict(self, sentence:str, labels:list, vocabulary:list, nlp):
        bag = self.bag_of_words(sentence, vocabulary, nlp)
        res = model.predict(np.array([bag]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': labels[r[0]], 'probability': str(r[1])})
        return return_list

    def get_response(self, intents_list, intents_json=intents):
        if len(intents_list) > 0:      
            tag = intents_list[0]['intent']
            list_of_intents = intents_json['intents']
            for i in list_of_intents:
                if i['tag'] == tag:
                    return random.choice(i['responses'])
        else:
            return "Sorry! I don't understand that question!"