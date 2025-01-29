#!/bin/bash
echo "🔹 Atualizando pacotes e instalando FFmpeg..."
apt-get update && apt-get install -y ffmpeg

echo "✅ FFmpeg instalado com sucesso. Iniciando aplicação..."
python3 main.py
