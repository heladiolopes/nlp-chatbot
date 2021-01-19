# Chatbot NLP

Protótipo de chatbot inteligente utilizando NLP e Rede Neural.

## Executando
O chatbot desenvolvido é dividido em duas aplicações. A primeira é uma aplicação servidor onde são executados os códigos de treinamento do chatbot e da api que retorna as respostas. A segunda é o script responsável por executar a aplicação cliente do chatbot, é nela que serão chamadas as requisições a api e o usuário irá conversar com o bot. Para executá-las basta seguir as instruções a seguir.

### API
Para iniciar a API há duas formas. A primeira, e mais simples, é via container docker, assim é necessário ter o docekr e o docker-compose instalado em sua máquina. Ao compilar o container será executado o script de treinamento do chatbot, então pode demorar um pouco. No diretório `/backend/` compile e execute o container com o comando a seguir.

```{bash}
$ docker-compose up --build -d
```

A segunda forma não envolve o docker, mas é necessário instalar as dependências localmente na sua máquina. Primeiramente, crie e ative um virtual enviroment com o comando a seguir.

```{bash}
$ python3 -m venv venv
$ source venv/bin/activate
```

Depois é necessário instalar as dependências do python e o modelo de dados do spacy.

```{bash}
$ pip3 install -r requirements.txt
$ python3 -m spacy download en_core_web_md
```

Por fim treine o chatbot e inicie o servidor. No diretório `/backend/` execute os comandos a seguir.

```{bash}
$ python3 api/train.py
$ gunicorn -w 4 -b 0.0.0.0:3001 run:app
```

### Client
Para executar a aplciação cliente é necessário ter o python com a biblioteca requests instalado. Em seguida apenas execute o script `client.py`.

```{bash}
$ pip3 install requests
$ python3 client.py
```
