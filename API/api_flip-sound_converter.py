from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import uuid
import threading
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configurações
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'aac', 'flac', 'mp4', 'mkv', 'avi', 'mov', 'webm'}

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

# Configurações de conversão específicas por formato
CONVERSION_PARAMS = {
    "Áudio - MP3": ["-c:a", "libmp3lame", "-b:a", "320k"],
    "Áudio - AAC": ["-c:a", "aac", "-b:a", "256k"],
    "Áudio - WAV": ["-c:a", "pcm_s16le"],
    "Áudio - FLAC": ["-c:a", "flac"],
    "Áudio - OGG": ["-c:a", "libvorbis", "-q:a", "6"],
    "Vídeo - MP4": ["-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-b:a", "192k"],
    "Vídeo - MKV": ["-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-b:a", "192k"],
    "Vídeo - AVI": ["-c:v", "libxvid", "-q:v", "7", "-c:a", "mp3", "-b:a", "192k"],
    "Vídeo - MOV": ["-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-b:a", "192k"],
    "Vídeo - WebM": ["-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0", "-c:a", "libopus", "-b:a", "128k"],
    "Vídeo - DivX": ["-c:v", "mpeg4", "-vtag", "DIVX", "-b:v", "1500k", "-c:a", "mp3", "-b:a", "192k"],
}

# Monitoramento de tarefas
tarefas_ativas = {}
lock = threading.Lock()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def limpar_arquivos_antigos():
    """Limpa arquivos que possam ter ficado para trás"""
    for arquivo in os.listdir(UPLOAD_FOLDER):
        caminho = os.path.join(UPLOAD_FOLDER, arquivo)
        try:
            if os.path.isfile(caminho):
                os.remove(caminho)
        except Exception as e:
            app.logger.error(f"Erro ao remover arquivo {caminho}: {e}")

def gerar_nome_arquivo(formato):
    """Gera um nome de arquivo único"""
    return os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}{FORMATOS[formato]}")

@app.route('/converter', methods=['POST'])
def converter_arquivo():
    # Garante que o diretório de upload existe
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Verifica se o arquivo foi enviado
    if 'arquivo' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files['arquivo']
    if arquivo.filename == '':
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
    
    if not allowed_file(arquivo.filename):
        return jsonify({"erro": "Tipo de arquivo não suportado"}), 400
    
    formato = request.form.get('formato', 'Áudio - MP3')
    
    # Valida o formato
    if formato not in FORMATOS:
        return jsonify({"erro": "Formato inválido"}), 400
    
    # Gera IDs únicos para entrada e saída
    task_id = str(uuid.uuid4())
    nome_entrada = os.path.join(UPLOAD_FOLDER, secure_filename(f"{task_id}_entrada_{arquivo.filename}"))
    nome_saida = gerar_nome_arquivo(formato)
    
    # Registra a tarefa
    with lock:
        tarefas_ativas[task_id] = {"status": "iniciando", "entrada": nome_entrada, "saida": nome_saida}
    
    try:
        # Salva o arquivo de entrada
        arquivo.save(nome_entrada)
        
        # Atualiza status
        with lock:
            tarefas_ativas[task_id]["status"] = "convertendo"
        
        # Obter parâmetros específicos de conversão
        params = CONVERSION_PARAMS.get(formato, [])
        
        # Comando básico de conversão
        command = ["ffmpeg", "-y", "-i", nome_entrada] + params + [nome_saida]
        
        # Executa conversão
        process = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Atualiza status
        with lock:
            tarefas_ativas[task_id]["status"] = "concluído"
        
        # Define nome para download
        nome_download = f"FlipSound_{formato.replace(' - ', '_')}{os.path.splitext(arquivo.filename)[1]}"
        
        # Retorna arquivo convertido
        return send_file(
            nome_saida, 
            as_attachment=True,
            download_name=nome_download
        )
    
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Erro de conversão: {e.stderr}")
        return jsonify({
            "erro": "Falha na conversão", 
            "detalhes": "O arquivo não pôde ser convertido para o formato solicitado."
        }), 500
    
    except Exception as e:
        app.logger.error(f"Erro geral: {str(e)}")
        return jsonify({"erro": "Erro interno do servidor"}), 500
    
    finally:
        # Limpa arquivos temporários
        try:
            if os.path.exists(nome_entrada):
                os.remove(nome_entrada)
            if os.path.exists(nome_saida):
                os.remove(nome_saida)
            
            # Remove a tarefa da lista
            with lock:
                if task_id in tarefas_ativas:
                    del tarefas_ativas[task_id]
        except Exception as e:
            app.logger.error(f"Erro na limpeza: {str(e)}")

@app.route('/status/<task_id>', methods=['GET'])
def verificar_status(task_id):
    """Verifica o status de uma conversão"""
    with lock:
        if task_id in tarefas_ativas:
            return jsonify({"status": tarefas_ativas[task_id]["status"]})
    return jsonify({"status": "não encontrado"}), 404

@app.route('/formatos', methods=['GET'])
def listar_formatos():
    """Retorna lista de formatos disponíveis"""
    formatos_audio = [f for f in FORMATOS.keys() if f.startswith("Áudio")]
    formatos_video = [f for f in FORMATOS.keys() if f.startswith("Vídeo")]
    
    return jsonify({
        "audio": formatos_audio,
        "video": formatos_video
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({"status": "ok"})

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"erro": f"Arquivo muito grande. Tamanho máximo: {MAX_CONTENT_LENGTH/1024/1024}MB"}), 413

# Configurar limite de tamanho de upload
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

if __name__ == '__main__':
    # Cria pasta para uploads se não existir
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Limpa arquivos antigos na inicialização
    limpar_arquivos_antigos()
    
    app.run(debug=True, port=5000)