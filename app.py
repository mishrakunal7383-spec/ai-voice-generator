from flask import Flask, request, jsonify, render_template
import edge_tts
import asyncio
import os

# 1️⃣ Flask app define
app = Flask(__name__)

# 2️⃣ Ensure static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

# 3️⃣ Voice Mapping: Language -> Mood -> Gender -> Neural Voice
voice_mapping = {
    "hi-IN": {
        "News Anchor": {"male": "hi-IN-PrabhatNeural", "female": "hi-IN-NeerjaNeural"},
        "Story Teller": {"male": "hi-IN-GauravNeural", "female": "hi-IN-AnanyaNeural"},
        "Cartoon": {"male": "hi-IN-ArjunNeural", "female": "hi-IN-SakshiNeural"},
        "Teacher": {"male": "hi-IN-RaghavNeural", "female": "hi-IN-MansiNeural"},
        "Crime Reporter": {"male": "hi-IN-PragyaNeural", "female": "hi-IN-RiyaNeural"},
        "Sant": {"male": "hi-IN-AaravNeural", "female": "hi-IN-AnikaNeural"},
        "Funny Kid": {"male": "hi-IN-RohanNeural", "female": "hi-IN-KiaraNeural"},
        "Aggressive": {"male": "hi-IN-KunalNeural", "female": "hi-IN-NishaNeural"},
        "Professional Anchor": {"male": "hi-IN-SameerNeural", "female": "hi-IN-PriyaNeural"},
        "Friendly Anchor": {"male": "hi-IN-VikramNeural", "female": "hi-IN-TanyaNeural"},
        "Devotional": {"male": "hi-IN-MohitNeural", "female": "hi-IN-ShrutiNeural"},
        "Motivational": {"male": "hi-IN-AdityaNeural", "female": "hi-IN-RiyaNeural"},
        "Advertisement": {"male": "hi-IN-RajNeural", "female": "hi-IN-AnanyaNeural"},
        "Excited": {"male": "hi-IN-ArnavNeural", "female": "hi-IN-MeeraNeural"},
        "Calm": {"male": "hi-IN-SachinNeural", "female": "hi-IN-TanviNeural"},
    },
    "gu-IN": {
        # Example placeholders, replace with actual gujarati voices
        "News Anchor": {"male": "gu-IN-Male1", "female": "gu-IN-Female1"},
        # ... add remaining moods for Gujarati
    },
    # Add remaining 13 languages similarly
}

# 4️⃣ Async function to generate voice with SSML for natural feel
async def generate_voice(text, voice):
    filename = "static/output.mp3"
    ssml_text = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
        <voice name="{voice}">
            <prosody rate="medium" pitch="medium">
                {text}
            </prosody>
        </voice>
    </speak>
    """
    communicate = edge_tts.Communicate(ssml_text, voice)
    await communicate.save(filename)
    return filename

# 5️⃣ Home route
@app.route("/")
def home():
    return render_template("index.html")

# 6️⃣ TTS route
@app.route("/tts", methods=["POST"])
def tts():
    try:
        text = request.form["text"]
        language = request.form["language"]
        mood = request.form["mood"]
        gender = request.form["gender"]

        if not text.strip():
            return jsonify({"error":"Text empty"}), 400

        if language not in voice_mapping or mood not in voice_mapping[language]:
            return jsonify({"error":"Voice not found"}), 400

        selected_voice = voice_mapping[language][mood][gender]

        asyncio.run(generate_voice(text, selected_voice))

        return jsonify({"audio": "static/output.mp3"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 7️⃣ Run app
if __name__ == "__main__":
    app.run()
