# ========================= IMPORTS =========================
import speech_recognition as sr
import webbrowser
import os
import subprocess
import queue
import pyttsx3
import music_lib
import time


# ========================= CONFIG =========================
WAKE_WORD = "alexa"

# ========================= TEXT TO SPEECH =========================
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

def speak(text):
    print(f"Assistant says: {text}")
    engine.say(text)
    engine.runAndWait()


def speak_and_confirm(text):
    speak(text)
    time.sleep(0.5)  # let audio finish


# ========================= SPEECH INPUT =========================
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source)

    try:
        print("Recognising...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()

    except sr.UnknownValueError:
        print("Could not understand")
        return ""

    except sr.RequestError:
        speak("Network error")
        return ""


# ========================= GENERAL APP / FILE OPENER =========================
def open_app_or_file(name):
    try:
        os.startfile(name)
    except Exception:
        try:
            subprocess.Popen(f'start "" {name}', shell=True)
        except Exception:
            speak("I could not open that")


# ========================= MUSIC PLAYER =========================
def play_music(song_name):
    song_name = song_name.lower()
    path = music_lib.music.get(song_name)

    if not path:
        speak("Song not found")
        return

    try:
        os.startfile(path)
    except Exception:
        speak("Unable to play the song")


# ========================= WAKE WORD LISTENER =========================
def start_wake_listener(wake_queue):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    def callback(recognizer, audio):
        try:
            text = recognizer.recognize_google(audio).lower()
            print(f"Background heard: {text}")
            if WAKE_WORD in text:
                wake_queue.put(True)
        except Exception:
            pass

    return recognizer.listen_in_background(mic, callback)


# ========================= MAIN PROGRAM =========================
if __name__ == "__main__":
    speak("Hello Sir, I am Roshan, your personal assistant.")

    wake_queue = queue.Queue()
    stop_listener = start_wake_listener(wake_queue)

    while True:
        # wait for wake word
        wake_queue.get()

        try:
            stop_listener()
        except Exception:
            pass

        speak("Yes?")
        command = take_command()

        stop_listener = start_wake_listener(wake_queue)

        if command == "":
            continue

        # -------- WEB --------
        if "open youtube" in command:
            speak_and_confirm("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif "open google" in command:
            speak_and_confirm("Opening Google")
            webbrowser.open("https://google.com")

        # -------- APPS / FILES --------
        elif command.startswith("open "):
            name = command.replace("open ", "").strip()
            speak_and_confirm(f"Opening {name}")
            open_app_or_file(name)

        # -------- MUSIC --------
        elif command.startswith("play "):
            song = command.replace("play ", "").strip()
            speak_and_confirm(f"Playing {song}")
            play_music(song)

        # -------- EXIT --------
        elif "exit" in command or "stop" in command or "quit" in command:
            speak_and_confirm("Goodbye")
            break
