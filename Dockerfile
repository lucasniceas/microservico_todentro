# Usa uma imagem base do Python 3.12
FROM python:3.12

# Instala FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os arquivos do projeto para o container
COPY . /app

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Define o comando para rodar o servidor Flask
CMD ["python", "main.py"]
