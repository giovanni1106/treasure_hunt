# Use uma imagem base do Python
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /code

# Copia o arquivo de requisitos para o container
COPY requirements.txt /code/

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o container
COPY . /code/

# Define a variável de ambiente
ENV PYTHONUNBUFFERED 1

# Expõe a porta 8000
EXPOSE 8000
