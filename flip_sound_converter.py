#!/usr/bin/env python3
import argparse
import subprocess
import os

def convert_media(input_file, output_file, extra_params=None):
    """
    Converte o arquivo de entrada para o formato desejado especificado em output_file.
    extra_params: lista de parâmetros adicionais para o FFmpeg (opcional).
    """
    # Comando básico: ffmpeg -y -i input_file [extra_params] output_file
    command = ["ffmpeg", "-y", "-i", input_file]
    if extra_params:
        command.extend(extra_params)
    command.append(output_file)
    
    print("Executando comando:")
    print(" ".join(command))
    
    # Executa o comando e verifica erros
    subprocess.run(command, check=True)

def main():
    parser = argparse.ArgumentParser(
        description="Conversor de mídia (áudio/vídeo) utilizando FFmpeg."
    )
    parser.add_argument("input", help="Caminho do arquivo de entrada")
    parser.add_argument("output", help="Caminho do arquivo de saída com a extensão desejada (ex.: output.mp3, output.mp4, etc.)")
    parser.add_argument(
        "--params", 
        nargs=argparse.REMAINDER, 
        help="Parâmetros adicionais para o FFmpeg (ex.: -ab 192k, -vf scale=1280:720)",
        default=[]
    )
    args = parser.parse_args()
    
    # Verifica se o arquivo de entrada existe
    if not os.path.isfile(args.input):
        print(f"Arquivo de entrada '{args.input}' não encontrado.")
        exit(1)
    
    try:
        convert_media(args.input, args.output, extra_params=args.params)
        print("Conversão concluída com sucesso!")
    except subprocess.CalledProcessError as e:
        print("Ocorreu um erro durante a conversão:")
        print(e)

if __name__ == '__main__':
    main()
