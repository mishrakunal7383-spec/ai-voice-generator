from flask import Flask, request, jsonify
import edge_tts
import asyncio
import os

app = Flask(__name__)

async def generate_voice(text, voice):
    filename = "static/output.mp3"  # static folder me save
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

    # Generate audio
    asyncio.run(generate_voice(text, voice))

    # Return path JSON me
    return jsonify({"audio": "static/output.mp3"})
