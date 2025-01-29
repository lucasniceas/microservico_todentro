import os
from pydub import AudioSegment
from .config import AUDIO_MAX_DURATION, OUTPUT_DIR

def mixar_audios(entrada_effect, meio_effect, audios_baixados, output_filename):
    """
    Junta os efeitos sonoros e os áudios baixados para criar um áudio final.

    Args:
        entrada_effect (str): Caminho do efeito de entrada.
        meio_effect (str): Caminho do efeito de transição.
        audios_baixados (list): Lista de caminhos de arquivos MP3 baixados.
        output_filename (str): Nome do arquivo de saída.

    Returns:
        str: Caminho do arquivo de áudio final.
    """
    try:
        combined_audio = AudioSegment.from_file(entrada_effect, format="mp3")

        for audio_path in audios_baixados:
            trecho_audio = AudioSegment.from_file(audio_path)[:AUDIO_MAX_DURATION * 1000]
            meio_effect_audio = AudioSegment.from_file(meio_effect, format="mp3")
            combined_audio += trecho_audio + meio_effect_audio

        output_path = os.path.join(OUTPUT_DIR, output_filename)
        combined_audio.export(output_path, format="mp3")

        print(f"Áudio final exportado: {output_path}")
        return output_path

    except Exception as e:
        raise ValueError(f"Erro ao mixar áudio: {e}")
