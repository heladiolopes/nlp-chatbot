from api import app
import os

HOST = os.getenv('API_HOST', '0.0.0.0')
PORT = os.getenv('API_PORT', '3001')
DEBUG = os.getenv('API_DEBUG', 'True') == 'True'

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)