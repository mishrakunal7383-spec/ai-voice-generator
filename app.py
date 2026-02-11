from flask import Flask, request, send_file
import edge_tts
import asyncio

app = Flask(__name__)

async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("output.mp3")

@app.route("/tts", methods=["POST"])
def tts():
    text = request.form["text"]
    voice = request.form["voice"]
    asyncio.run(generate_voice(text, voice))
    return send_file("output.mp3", as_attachment=True)

@app.route("/")
def home():
    return "AI Voice Generator Running 🚀"

if __name__ == "__main__":
    app.run()
