# Flask framework
from flask_restful import Resource, reqparse

# Outras dependências
import random


# Classe do chatbot
class Chatbot(Resource):
    
    def __init__(self):
        pass

    def get(self):
        return {'message': 'get'}, 200

    def post(self):
        return {'message': 'post'}, 200
