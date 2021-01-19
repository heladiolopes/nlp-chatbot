FROM python:3.7-buster

# Instalando dependências
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
RUN python3 -m spacy download en_core_web_md
RUN python3 -m spacy download pt_core_news_md

# Copiando arquivos
COPY ./api /api
COPY ./run.py /run.py

# Treinamento do modelo
RUN python3 /api/train.py
