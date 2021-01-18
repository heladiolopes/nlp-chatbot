# Flask framework
from flask import Flask
from flask_restful import Api

# Modulos
from .Chatbot import Chatbot

# Instaciar aplicação flask
app = Flask(__name__)
api = Api(app)

# Adicionar modulos
api.add_resource(Chatbot, '/chat')