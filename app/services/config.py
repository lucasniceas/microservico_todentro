import os

# Diretório onde os arquivos de saída serão armazenados
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configuração da qualidade do áudio
AUDIO_QUALITY = "192"  # Qualidade de saída (kbps)

# Tempo máximo de cada trecho de áudio (em segundos)
AUDIO_MAX_DURATION = 10

# Formato padrão de saída
DEFAULT_AUDIO_FORMAT = "mp3"
