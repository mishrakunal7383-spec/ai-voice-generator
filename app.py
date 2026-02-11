from flask import Flask, request, jsonify, render_template
import edge_tts
import asyncio
import os

# 1️⃣ Flask app define
app = Flask(__name__)

# 2️⃣ Ensure static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

# 3️⃣ Async function to generate voice
async def generate_voice(text, voice):
    filename = "static/output.mp3"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)
    return filename

# 4️⃣ Home route
@app.route("/")
def home():
    return render_template("index.html")

# 5️⃣ TTS route
@app.route("/tts", methods=["POST"])
def tts():
    try:
        text = request.form["text"]
        voice = request.form["voice"]
        if not text.strip():
            return jsonify({"error":"Text empty"}), 400

        # Generate audio
        asyncio.run(generate_voice(text, voice))

        # Return JSON path
        return jsonify({"audio": "static/output.mp3"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 6️⃣ Run app
if __name__ == "__main__":
    app.run()
