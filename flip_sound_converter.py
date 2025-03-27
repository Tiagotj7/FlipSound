import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os

# Lista de formatos suportados (extensão e tipo)
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
}

def selecionar_entrada():
    arquivo = filedialog.askopenfilename(title="Selecione o arquivo de entrada")
    if arquivo:
        entrada_var.set(arquivo)

def selecionar_saida():
    # Obtém a extensão escolhida pelo formato
    ext = FORMATOS.get(formato_var.get(), "")
    arquivo = filedialog.asksaveasfilename(title="Selecione o local para salvar o arquivo de saída",
                                           defaultextension=ext,
                                           filetypes=[("Arquivo convertido", "*" + ext)])
    if arquivo:
        saida_var.set(arquivo)

def converter():
    input_file = entrada_var.get()
    output_file = saida_var.get()
    
    if not input_file or not os.path.isfile(input_file):
        messagebox.showerror("Erro", "Selecione um arquivo de entrada válido!")
        return
    if not output_file:
        messagebox.showerror("Erro", "Selecione um arquivo de saída válido!")
        return
    
    # Comando básico: ffmpeg -y -i input_file output_file
    command = ["ffmpeg", "-y", "-i", input_file, output_file]
    try:
        log_text.delete(1.0, tk.END)
        log_text.insert(tk.END, "Executando comando:\n" + " ".join(command) + "\n")
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log_text.insert(tk.END, "Conversão concluída com sucesso!")
        messagebox.showinfo("Sucesso", "Conversão concluída com sucesso!")
    except subprocess.CalledProcessError as e:
        log_text.insert(tk.END, "Erro durante a conversão:\n" + str(e))
        messagebox.showerror("Erro", "Ocorreu um erro durante a conversão.")

# Configuração da interface com Tkinter
root = tk.Tk()
root.title("FlipSound - Conversor de Áudio/Video")

# Variáveis para armazenar caminhos e formato
entrada_var = tk.StringVar()
saida_var = tk.StringVar()
formato_var = tk.StringVar(value=list(FORMATOS.keys())[0])

# Frame para arquivo de entrada
frame_entrada = tk.Frame(root, pady=5)
frame_entrada.pack(fill=tk.X)
tk.Label(frame_entrada, text="Arquivo de Entrada:").pack(side=tk.LEFT, padx=5)
tk.Entry(frame_entrada, textvariable=entrada_var, width=50).pack(side=tk.LEFT, padx=5)
tk.Button(frame_entrada, text="Selecionar", command=selecionar_entrada).pack(side=tk.LEFT, padx=5)

# Frame para escolha do formato de saída
frame_formato = tk.Frame(root, pady=5)
frame_formato.pack(fill=tk.X)
tk.Label(frame_formato, text="Formato de Saída:").pack(side=tk.LEFT, padx=5)
combo = ttk.Combobox(frame_formato, textvariable=formato_var, values=list(FORMATOS.keys()), state="readonly", width=20)
combo.pack(side=tk.LEFT, padx=5)

# Frame para arquivo de saída
frame_saida = tk.Frame(root, pady=5)
frame_saida.pack(fill=tk.X)
tk.Label(frame_saida, text="Arquivo de Saída:").pack(side=tk.LEFT, padx=5)
tk.Entry(frame_saida, textvariable=saida_var, width=50).pack(side=tk.LEFT, padx=5)
tk.Button(frame_saida, text="Selecionar", command=selecionar_saida).pack(side=tk.LEFT, padx=5)

# Botão de conversão
btn_converter = tk.Button(root, text="Converter", command=converter, width=20, bg="#4CAF50", fg="white")
btn_converter.pack(pady=10)

# Área para log
log_text = tk.Text(root, height=10, width=80)
log_text.pack(padx=5, pady=5)

root.mainloop()
