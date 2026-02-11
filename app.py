from flask import Flask, request, jsonify, render_template
from gtts import gTTS
import os

app = Flask(__name__, static_url_path="/static", static_folder="static", template_folder="templates")

# Ensure static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

# Define moods
moods = [
    "News Anchor", "Story Teller", "Cartoon", "Teacher", "Crime Reporter",
    "Sant", "Funny Kid", "Aggressive", "Professional Anchor", "Friendly Anchor",
    "Devotional", "Motivational", "Advertisement", "Excited", "Calm"
]

# Define voices mapping for simulation
voices = ["male", "female", "kid"]  # gTTS cannot change voice, just simulate
languages = ["hi", "en"]

@app.route("/")
def home():
    return render_template("index.html", moods=moods, voices=voices, languages=languages)

@app.route("/tts", methods=["POST"])
def tts():
    text = request.form.get("text", "").strip()
    lang = request.form.get("language", "hi")
    voice_type = request.form.get("voice", "male")
    mood = request.form.get("mood", "News Anchor")

    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400
    if lang not in languages:
        lang = "hi"
    if voice_type not in voices:
        voice_type = "male"
    if mood not in moods:
        mood = "News Anchor"

    # filename
    filename = "output.mp3"
    filepath = os.path.join("static", filename)

    # Append voice/mood in text for simulation
    tts_text = f"[{mood} | {voice_type.upper()}] {text}"

    try:
        tts = gTTS(text=tts_text, lang=lang)
        tts.save(filepath)
        return jsonify({"audio": f"/static/{filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
