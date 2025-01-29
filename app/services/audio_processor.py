import os
import logging
from pydub import AudioSegment
import requests
from gtts import gTTS
from .youtube_downloader import baixar_audio

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Exibe logs no terminal
    ]
)

def validar_link(link):
    """
    Verifica se o link é válido e acessível.

    Args:
        link (str): URL do vídeo no YouTube.

    Returns:
        bool: True se o link for válido, False caso contrário.
    """
    try:
        response = requests.head(link, allow_redirects=True, timeout=5)
        if response.status_code != 200:
            logging.warning(f"⚠️ Link inválido: {link} (Status: {response.status_code})")
            return False
        return True
    except requests.RequestException as e:
        logging.error(f"❌ Erro ao validar link {link}: {e}")
        return False

def gerar_audio_convite(texto, destino):
    """
    Converte o texto do convite em áudio e salva no destino especificado.

    Args:
        texto (str): Texto a ser falado no convite.
        destino (str): Caminho onde o arquivo de áudio será salvo.

    Returns:
        str: Caminho do arquivo gerado.
    """
    try:
        if not texto.strip():
            raise ValueError("❌ O texto do convite está vazio.")

        tts = gTTS(texto, lang="pt")
        tts.save(destino)
        logging.info(f"✅ Áudio do convite gerado: {destino}")
        return destino
    except Exception as e:
        raise ValueError(f"❌ Erro ao gerar áudio do convite: {e}")

def process_audio(data: dict):
    """
    Processa o áudio com base nos dados recebidos.

    Args:
        data (dict): Dados contendo gênero musical, texto do convite e informações do evento.

    Returns:
        dict: Resumo do processamento realizado.
    """
    logging.info("🔹 Iniciando processamento do áudio...")

    genero = data.get("generoMusical")
    texto_convite = data.get("textoConvite")
    dados_evento = data.get("dadosEvento", {})

    if not genero or not texto_convite or not dados_evento:
        logging.warning("⚠️ Dados inválidos recebidos! Verifique 'generoMusical', 'textoConvite' e 'dadosEvento'.")
        return {"error": "Faltam dados essenciais: 'generoMusical', 'textoConvite' ou 'dadosEvento'."}, 400

    # Verifica se nomePessoa está presente nos dados do evento
    nome_pessoa = dados_evento.get("nomePessoa")
    if not nome_pessoa:
        logging.warning("⚠️ Campo 'nomePessoa' não fornecido dentro de 'dadosEvento'.")
        return {"error": "O campo 'nomePessoa' dentro de 'dadosEvento' é obrigatório."}, 400

    logging.info(f"🎵 Processando áudio para {nome_pessoa} - Gênero: {genero}")

    links_musicas = data.get("linksMusicas", [])

    # Diretório base dos arquivos de áudio
    base_dir = os.path.join("app", "assets", genero)

    # Valida se o gênero existe
    if not os.path.exists(base_dir):
        logging.error(f"❌ Gênero musical '{genero}' não encontrado!")
        return {"error": f"Gênero musical '{genero}' não encontrado no servidor."}, 400

    # Verificar as pastas `entrada` e `meio`
    entrada_dir = os.path.join(base_dir, "entrada")
    meio_dir = os.path.join(base_dir, "meio")

    if not os.path.exists(entrada_dir) or not os.path.exists(meio_dir):
        logging.error(f"❌ Pastas de efeitos sonoros para '{genero}' estão incompletas!")
        return {"error": f"Efeitos para o gênero '{genero}' estão incompletos."}, 400

    try:
        logging.info("📂 Carregando efeitos de áudio...")
        entrada_effect = AudioSegment.from_file(os.path.join(entrada_dir, "big-fone-atencao.mp3"))
        meio_effect = AudioSegment.from_file(os.path.join(meio_dir, "irra-ratinho.mp3"))

        combined_audio = entrada_effect

        # Gerar e adicionar o áudio do convite falado
        convite_path = "convite.mp3"
        logging.info("🔊 Gerando áudio do convite...")
        gerar_audio_convite(texto_convite, convite_path)
        convite_audio = AudioSegment.from_file(convite_path)
        combined_audio += convite_audio

        # Baixar e processar os áudios dos links fornecidos
        arquivos_baixados = []
        for idx, link in enumerate(links_musicas):
            destino = f"temp_audio_{idx}.mp3"

            # Validar se o link é acessível antes do download
            if not validar_link(link):
                logging.warning(f"⚠️ Link inválido ou inacessível: {link}")
                return {"error": f"Link inválido ou inacessível: {link}"}, 400

            logging.info(f"⬇️ Baixando áudio: {link}")
            caminho_audio = baixar_audio(link, destino=destino)
            arquivos_baixados.append(caminho_audio)

            # Carregar trecho de 30 segundos do áudio baixado
            trecho_audio = AudioSegment.from_file(caminho_audio)
            trecho_audio = trecho_audio[:30 * 1000]  # Recorta apenas 30 segundos

            # Adiciona ao áudio combinado com efeito intermediário
            combined_audio += trecho_audio + meio_effect

        # Efeito final para encerrar
        efeito_final = AudioSegment.silent(duration=2000)  # 2 segundos de silêncio
        combined_audio += efeito_final

        # Exportar áudio processado
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{nome_pessoa}_final.mp3")
        combined_audio.export(output_path, format="mp3")

        logging.info(f"✅ Áudio gerado com sucesso: {output_path}")

        return {
            "genero": genero,
            "texto_convite": texto_convite,
            "dados_evento": dados_evento,
            "links_musicas": links_musicas,
            "arquivos_baixados": arquivos_baixados,
            "status": "Áudio processado e exportado com sucesso.",
            "output_path": output_path
        }, 200
    except Exception as e:
        logging.error(f"❌ Erro ao processar o áudio: {e}")
        return {"error": f"Erro ao processar o áudio: {e}"}, 500

# Definir caminho manualmente para o FFmpeg
AudioSegment.converter = "/usr/bin/ffmpeg"
AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
AudioSegment.ffprobe = "/usr/bin/ffprobe"