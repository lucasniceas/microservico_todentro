import os
from yt_dlp import YoutubeDL
from .config import DEFAULT_AUDIO_FORMAT, AUDIO_QUALITY

def baixar_audio(link, destino):
    """
    Baixa e extrai o áudio de um vídeo do YouTube.

    Args:
        link (str): URL do vídeo no YouTube.
        destino (str): Caminho onde o áudio será salvo.

    Returns:
        str: Caminho do arquivo de áudio baixado.

    Raises:
        ValueError: Se o download falhar.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': DEFAULT_AUDIO_FORMAT,
            'preferredquality': AUDIO_QUALITY,
        }],
        'outtmpl': destino
    }

    try:
        print(f"🔹 Baixando áudio do link: {link}")
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            if not info:
                raise ValueError(f"⚠️ Erro: Nenhuma informação de vídeo foi obtida para o link: {link}")

        if not os.path.exists(destino):
            raise ValueError(f"⚠️ Erro: Arquivo não foi baixado corretamente - {destino}")

        print(f"✅ Download concluído: {destino}")
        return destino

    except Exception as e:
        raise ValueError(f"❌ Erro ao baixar áudio: {e}")