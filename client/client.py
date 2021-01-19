import requests as req
import json
import os

base_url = os.getenv('BASE_URL', 'http://localhost:3001')

def get_chatbot_response(message):
    data = json.dumps({"message": message})
    headers = {'Content-Type': 'application/json'}
    
    response = req.post(f"{base_url}/chat", headers=headers, data=data)

    return response.json()["message"]


if __name__ == '__main__':
    
    # Executar chatbot na linha de comando
    while True:
        message = input("USER >> ")
        response = get_chatbot_response(message)
        
        print(" BOT >> {0}".format(response))
