import speech_recognition as sr
import requests
import pyttsx3
import pyjokes
import datetime
import wikipedia
import webbrowser
import os
from ytmusicapi import YTMusic
import yt_dlp
import vlc


# =========================
# LOAD ENV
# =========================


NEWS_API_KEY = 
WEATHER_API_KEY = 

# =========================
# TTS
# =========================

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# =========================
# MUSIC
# =========================

ytmusic = YTMusic()

# =========================
# AI MODEL
# =========================

# =========================
# SPEAK
# =========================

def speak(audio):
    print(f"Jarvis: {audio}")

    engine.say(audio)
    engine.runAndWait()


# =========================
# MUSIC
# =========================

def play_music(query):
    try:
        speak(f"Playing {query}")

        results = ytmusic.search(query, filter="songs")

        if not results:
            speak("No song found")
            return

        video_id = results[0]["videoId"]

        url = f"https://youtube.com/watch?v={video_id}"

        ydl_opts = {
            "format": "bestaudio",
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            play_url = info["url"]

        player = vlc.MediaPlayer(play_url)
        player.play()

    except Exception as e:
        print(e)
        speak("Unable to play music")

# =========================
# WEATHER
# =========================

def weather(city):
    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )

        response = requests.get(url)

        data = response.json()

        temp = data["main"]["temp"]

        desc = data["weather"][0]["description"]

        speak(f"Temperature is {temp} degree celsius")
        speak(f"Weather is {desc}")

    except Exception as e:
        print(e)
        speak("Weather error")

# =========================
# NEWS
# =========================

def news():
    try:
        url = (
            f"https://newsapi.org/v2/top-headlines?"
            f"country=us&category=technology&apiKey={NEWS_API_KEY}"
        )

        response = requests.get(url)

        data = response.json()

        articles = data["articles"][:5]

        speak("Top technology news")

        for article in articles:
            title = article["title"]

            print(title)

            speak(title)

    except Exception as e:
        print(e)
        speak("News error")

# =========================
# TIME
# =========================

def tell_time():
    current = datetime.datetime.now().strftime("%I:%M %p")

    speak(f"The time is {current}")

# =========================
# JOKE
# =========================

def tell_joke():
    joke = pyjokes.get_joke()

    speak(joke)

# =========================
# GREETING
# =========================

def wishme():
    hour = datetime.datetime.now().hour

    if hour < 12:
        speak("Good morning")

    elif hour < 18:
        speak("Good afternoon")

    else:
        speak("Good evening")

# =========================
# LISTEN
# =========================

def commandintake():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        r.pause_threshold = 1

        audio = r.listen(source)

    try:
        print("Recognizing...")

        query = r.recognize_google(audio, language="en-in")

        print("User:", query)

        return query.lower()

    except Exception as e:
        print(e)

        return ""

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    speak("Initializing Jarvis")

    wishme()

    while True:

        command = commandintake()

        if not command:
            continue

        if "exit" in command:
            speak("Goodbye")
            break

        if "time" in command:
            tell_time()

        if "joke" in command:
            tell_joke()

        if "play" in command:
            song = command.replace("play", "")

            play_music(song)

        if "weather" in command:
            speak("Tell city name")

            city = commandintake()

            weather(city)

        if "news" in command:
            news()

        if "search" in command:
            query = command.replace("search", "")

            webbrowser.open(
                f"https://google.com/search?q={query}"
            )

        if "what is" in command or "who is" in command:
            try:
                result = wikipedia.summary(command, sentences=2)

                speak(result)

            except:
                speak("No result found")
