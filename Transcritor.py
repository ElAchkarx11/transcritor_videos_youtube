# Importação de bibliotecas que baixam o áudio do Youtube
from pytubefix import YouTube
from pytubefix.cli import on_progress
# Importação de bibliotecas que fazem a transcrição do áudio
import whisper
# Importação de bibliotecas que fazem a conexão com a API do Gemini
from google import genai
from google.genai import types
# Importação de bibliotecas que ajudam a carregar variáveis de ambiente
from dotenv import load_dotenv
import os
# Importação de bibliotecas do Flask para criar a aplicação web
from flask import Flask
from flask import request, render_template

#resgatando valores do .env
load_dotenv()

app = Flask(__name__, template_folder= "templates")

@app.route("/", methods=['POST', 'GET'])
def Transcritor():
    if request.method == "POST":
        #Digito a minha url desejada
        url = request.form['url']

        #Defino qual vai ser o nome do meu arquivo criado
        filename_audio = "Audio.mp3"
        #Criando o objeto de Youtube
        yt = YouTube(url, on_progress_callback=on_progress, client="WEB")

        #Aqui digo que somete quero o audio do vídeo que estou mandando
        ys = yt.streams.get_audio_only()
        #Faço o Download desse arquivo e digo que o nome dele vai ser igual ao que digitei antes
        ys.download(filename=filename_audio, output_path="downloads")

        #Aqui estou usando o whisper e dizendo para que ele pegue um modelo base
        model = whisper.load_model("base")
        #O vídeo é transcrito pela ia, que é passada para a próxima fase do processo
        result = model.transcribe(filename_audio)

        #Configura o client utilizando a chave de api do Gemini do Google(Deixando a API oculta)
        client = genai.Client(api_key=os.getenv('GEMINY_API_KEY'))

        #configuro o modelo do gemini que estarei utilizando, o que eu vou gerar e o que vou interpretar
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Resuma " + result["text"],
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0) #Evitando o uso desnecessário de processamento, desativa algumas funcionalidades de pensamento
            ),
        ) 
        return render_template('Resumo.html') #Renderiza a página de resumo com o resultado
    return render_template('Transcritor.html') # Renderiza a página inicial do transcritor
