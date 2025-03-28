from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import uuid

app = Flask(__name__)
CORS(app)

# Dicionário de formatos suportados
FORMATOS = {
    "Áudio - MP3": ".mp3",
    "Áudio - AAC": ".aac",
    "Áudio - WAV": ".wav",
    "Áudio - FLAC": ".flac",
    "Áudio - OGG": ".ogg",
    "Vídeo - MP4": ".mp4",
    "Vídeo - MKV": ".mkv",
    "Vídeo - AVI": ".avi",
    "Vídeo - MOV": ".mov",
    "Vídeo - WebM": ".webm",
    "Vídeo - DivX": ".avi",
}

def gerar_nome_arquivo(formato):
    """Gera um nome de arquivo único"""
    return f"uploads/{uuid.uuid4()}{FORMATOS[formato]}"

@app.route('/converter', methods=['POST'])
def converter_arquivo():
    # Verifica se o arquivo foi enviado
    if 'arquivo' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files['arquivo']
    formato = request.form.get('formato', 'Áudio - MP3')
    
    # Valida o formato
    if formato not in FORMATOS:
        return jsonify({"erro": "Formato inválido"}), 400
    
    # Salva o arquivo de entrada
    nome_entrada = f"uploads/{uuid.uuid4()}_{arquivo.filename}"
    arquivo.save(nome_entrada)
    
    # Gera nome para arquivo de saída
    nome_saida = gerar_nome_arquivo(formato)
    
    # Comando de conversão
    if formato == "Vídeo - DivX":
        command = [
            "ffmpeg", "-y", "-i", nome_entrada,
            "-c:v", "mpeg4", "-vtag", "DIVX", "-b:v", "1500k",
            "-c:a", "mp3", "-b:a", "192k",
            nome_saida
        ]
    else:
        command = ["ffmpeg", "-y", "-i", nome_entrada, nome_saida]
    
    try:
        # Executa conversão
        subprocess.run(command, check=True, capture_output=True)
        
        # Retorna arquivo convertido
        return send_file(nome_saida, as_attachment=True)
    
    except subprocess.CalledProcessError as e:
        return jsonify({
            "erro": "Falha na conversão", 
            "detalhes": str(e.stderr)
        }), 500
    finally:
        # Limpa arquivos temporários
        if os.path.exists(nome_entrada):
            os.remove(nome_entrada)
        if os.path.exists(nome_saida):
            os.remove(nome_saida)

@app.route('/formatos', methods=['GET'])
def listar_formatos():
    """Retorna lista de formatos disponíveis"""
    return jsonify(list(FORMATOS.keys()))

if __name__ == '__main__':
    # Cria pasta para uploads se não existir
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, port=5000)