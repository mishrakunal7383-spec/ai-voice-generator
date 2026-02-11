from flask import Flask, request, jsonify, render_template
import edge_tts
import asyncio
import os

app = Flask(__name__)

# Ensure static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

async def generate_voice(text, voice):
    filename = "static/output.mp3"  # Save audio in static folder
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

    # Return JSON path
    return jsonify({"audio": "static/output.mp3"})

if __name__ == "__main__":
    app.run()
