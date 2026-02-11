from flask import render_template

@app.route("/tts", methods=["POST"])
def tts():
    text = request.form["text"]
    voice = request.form["voice"]

    asyncio.run(generate_voice(text, voice))

    return render_template("index.html", audio="output.mp3")
