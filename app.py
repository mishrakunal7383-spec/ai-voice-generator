from flask import Flask, request, send_file, render_template
import edge_tts
import asyncio
import os

app = Flask(__name__)

async def generate_voice(text, voice):
    filename = "output.mp3"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)
    return filename

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts():
    text = request.form["text"]
    voice = request.form["voice"]
    filename = asyncio.run(generate_voice(text, voice))
    
    if os.path.exists(filename):
        audio_path = filename
    else:
        audio_path = None

    return render_template("index.html", audio=audio_path)

if __name__ == "__main__":
    app.run()
