from flask import Flask, request, jsonify, render_template
from gtts import gTTS
import os

app = Flask(__name__, static_url_path="/static", static_folder="static", template_folder="templates")

# Ensure static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts():
    text = request.form.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400

    filename = "output.mp3"
    filepath = os.path.join("static", filename)

    try:
        # Natural Hindi female voice
        tts = gTTS(text=text, lang="hi")
        tts.save(filepath)
        return jsonify({"audio": f"/static/{filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
