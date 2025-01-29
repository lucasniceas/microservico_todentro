#!/bin/bash

# Atualiza os pacotes do sistema
apt-get update 

# Instala o ffmpeg
apt-get install -y ffmpeg 

# Inicia o aplicativo Python
python3 main.py
