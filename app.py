from flask import Flask, request, jsonify, render_template
from gtts import gTTS
import os

app = Flask(__name__)

# ensure static folder
if not os.path.exists("static"):
    os.makedirs("static")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts():
    try:
        text = request.form.get("text", "").strip()
        lang = request.form.get("language", "hi")

        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400

        # filename
        filename = "static/output.mp3"

        # create tts
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)

        return jsonify({"audio": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
