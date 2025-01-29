FROM python:3.12

# Instalar ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Criar e ativar um ambiente virtual (opcional)
WORKDIR /app
COPY . /app

# Instalar dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Definir variável de ambiente para evitar buffer no Flask
ENV PYTHONUNBUFFERED=1

# Comando para rodar o app
CMD ["python", "main.py"]
