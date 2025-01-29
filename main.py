import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from app.services.audio_processor import process_audio
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Diretório onde os áudios são salvos
OUTPUT_DIR = "output"

@app.route("/")
def home():
    """
    Rota principal para verificar se o serviço está online.
    """
    return jsonify({"message": "Microserviço de áudio está rodando!"})

@app.route("/process_audio", methods=["POST"])
def process_audio_route():
    """
    Rota para processar áudio com base nos dados enviados pelo cliente.
    
    Requer:
        JSON contendo os dados de entrada no corpo da requisição.
    
    Retorna:
        JSON com o resumo do processamento.
    """
    try:
        data = request.get_json()
        print("🔹 Dados recebidos:", data)  # <-- Log para debug

        if not data:
            return jsonify({"error": "Dados não fornecidos na requisição."}), 400
        
        required_keys = ["generoMusical", "textoConvite", "dadosEvento", "linksMusicas"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"'{key}' é obrigatório na entrada."}), 400

        # Processar o áudio usando o serviço
        response = process_audio(data)
        return jsonify(response), 200
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")  # <-- Log para debug de erro
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

@app.route("/audios", methods=["GET"])
def listar_audios():
    """
    Lista todos os arquivos de áudio gerados.
    """
    try:
        if not os.path.exists(OUTPUT_DIR):
            return jsonify({"error": "Diretório de saída não encontrado."}), 500

        arquivos = os.listdir(OUTPUT_DIR)
        arquivos_mp3 = [arquivo for arquivo in arquivos if arquivo.endswith(".mp3")]
        return jsonify({"audios": arquivos_mp3}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao listar áudios: {str(e)}"}), 500

@app.route("/download/<filename>", methods=["GET"])
def baixar_audio(filename):
    """
    Permite baixar um arquivo de áudio específico pelo nome.
    """
    try:
        return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "Arquivo não encontrado."}), 404
    except Exception as e:
        return jsonify({"error": f"Erro ao baixar o arquivo: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
