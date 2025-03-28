# FlipSound - Conversor de Áudio/Video

FlipSound é um aplicativo desktop simples, elegante e poderoso para conversão de arquivos de áudio e vídeo utilizando o FFmpeg. Desenvolvido em Python com interface gráfica em Tkinter, o FlipSound oferece uma solução rápida e intuitiva para transformar seus arquivos multimídia para os formatos mais populares – inclusive DivX!

---

## 🚀 Visão Geral

O **FlipSound** foi criado para facilitar a conversão de arquivos, permitindo que você:
- Selecione um arquivo de entrada com facilidade.
- Escolha o formato de saída desejado entre os mais usados (MP3, AAC, WAV, FLAC, OGG, MP4, MKV, AVI, MOV, WebM e DivX).
- Realize a conversão automaticamente, gerando um novo arquivo com a extensão apropriada.

O projeto é ideal para estúdios, profissionais de edição e entusiastas que precisam de uma ferramenta prática para conversão de mídia.

---

## 🎯 Funcionalidades

- **Interface Intuitiva:** Seleção de arquivo de entrada e escolha de formato de saída via interface gráfica.
- **Suporte a Múltiplos Formatos:** Converte para os formatos de áudio e vídeo mais populares, incluindo suporte especial para conversão para DivX.
- **Automação da Conversão:** Geração automática do nome do arquivo de saída com a extensão correspondente.
- **Feedback Visual:** Área de log que exibe os comandos executados e status da conversão.
- **Integração com FFmpeg:** Utiliza a robusta ferramenta FFmpeg para garantir conversões rápidas e de alta qualidade.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3:** Linguagem de programação principal.
- **Tkinter:** Biblioteca padrão para interfaces gráficas em Python.
- **FFmpeg:** Ferramenta de linha de comando para conversão de áudio e vídeo.
- **Subprocess:** Módulo para invocar comandos do sistema.

---

## ⚙️ Instalação

### Pré-requisitos

1. **Python 3** – Certifique-se de ter o Python 3 instalado no seu sistema.
2. **FFmpeg** – Instale o FFmpeg e adicione-o ao PATH do sistema.
   - **Windows 11:**
     - Baixe o FFmpeg [aqui](https://ffmpeg.org/download.html) (recomendamos builds do [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)).
     - Extraia o arquivo para um diretório (por exemplo, `C:\ffmpeg`) e adicione o caminho `C:\ffmpeg\bin` às variáveis de ambiente.
   - **Linux:**
     ```bash
     sudo apt update && sudo apt install ffmpeg -y
     ```
   - **macOS:**
     ```bash
     brew install ffmpeg
     ```

### Clone o Repositório

```bash
git clone https://github.com/seu-usuario/flip-sound.git
cd flip-sound
```

---

## 📂 Uso

Basta executar o script Python para abrir a interface gráfica:

```bash
python flip_sound_gui.py
```

### Passo a Passo

1. **Selecione o Arquivo de Entrada:**  
   Clique no botão **"Selecionar"** e escolha o arquivo de mídia que deseja converter.

2. **Escolha o Formato de Saída:**  
   No menu dropdown, escolha entre os formatos disponíveis, inclusive **"Vídeo - DivX"**.

3. **Converter:**  
   Clique em **"Converter"**. O aplicativo gera automaticamente o nome do arquivo de saída e executa a conversão utilizando FFmpeg.

4. **Visualize o Log:**  
   A área de log exibirá o comando executado e o status da conversão.

---

## 🎨 Demonstração

![FlipSound Demo](https://raw.githubusercontent.com/Tiagotj7/FlipSound/main/assets/flip_logo.png)

*Exemplo da interface gráfica do FlipSound em ação.*

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para sugerir melhorias.

---

## 📜 Licença

Distribuído sob a Licença MIT. Veja o arquivo [LICENSE](https://github.com/Tiagotj7/FlipSound/blob/main/LICENSE) para mais detalhes ou consulte [informações sobre a Licença MIT](https://opensource.org/licenses/MIT).

---

## 📞 Contato

**Desenvolvedor:** Tiagotj7  
**E-mail:** tiagotj7dev@gmail.com  
**LinkedIn:** [Tiago Carvalho](https://www.linkedin.com/in/tiagocarvalhog2020/)  
**GitHub:** [Tiagotj7](https://github.com/Tiagotj7/FlipSound)

---

FlipSound é a solução ideal para quem busca uma ferramenta simples, eficiente e moderna para conversão de mídia. Transforme seus arquivos com qualidade e agilidade!🔊🎶🎚️
