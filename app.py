from flask import Flask, request, send_file, render_template
import edge_tts
import asyncio

app = Flask(__name__)

async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("output.mp3")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts():
    text = request.form["text"]
    voice = request.form["voice"]

    asyncio.run(generate_voice(text, voice))

    return render_template("index.html", audio="output.mp3")

if __name__ == "__main__":
    app.run()
