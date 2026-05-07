from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import jarvis

app = Flask(__name__)

CORS(app)

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():

    data = request.json

    text = data["message"].lower()

    response = "Command not recognized"

    # =========================
    # GREET
    # =========================
    
    if "hello" or "hey" in text:
        response = "Hey, Boss How are you !!?"
    # =========================
    # TIME
    # =========================

    if "time" in text:

        response = jarvis.tell_time()

    # =========================
    # JOKE
    # =========================

    elif "joke" in text:

        response = jarvis.tell_joke()

    # =========================
    # PLAY MUSIC
    # =========================

    elif "play" in text:
        song = text.replace("play", "").strip()
        response = jarvis.play_music(song)

    # =========================
    # WEATHER
    # =========================

    elif "weather" in text:

        city = text.replace("weather", "").strip()

        response = jarvis.weather(city)

    # =========================
    # NEWS
    # =========================

    elif "news" in text:

        headlines = jarvis.news()

        response = " . ".join(headlines)

    # =========================
    # SEARCH
    # =========================

    elif "search" in text:

        query = text.replace("search", "").strip()

        import webbrowser

        webbrowser.open(
            f"https://google.com/search?q={query}"
        )

        response = f"Searching for {query}"

    # =========================
    # WIKIPEDIA
    # =========================

    elif "what is" in text or "who is" in text:

        response = jarvis.wikipedia_search(text)

    return jsonify({
        "response": response
    })

if __name__ == "__main__":

    app.run(debug=True)