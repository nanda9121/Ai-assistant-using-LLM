import os

try:
    import pyttsx3
    import speech_recognition as sr
except ImportError as error:
    pyttsx3 = None
    sr = None
    AUDIO_IMPORT_ERROR = error
else:
    AUDIO_IMPORT_ERROR = None

_engine = None


def speak(text):
    global _engine
    print(f"JARVIS: {text}")
    if pyttsx3 is None:
        print(f"Speech output is unavailable: {AUDIO_IMPORT_ERROR}")
        return

    try:
        if _engine is None:
            _engine = pyttsx3.init()
            _engine.setProperty("rate", int(os.getenv("ASSISTANT_SPEECH_RATE", "165")))
        _engine.say(text)
        _engine.runAndWait()
    except (RuntimeError, OSError) as error:
        _engine = None
        print(f"Speech output is unavailable: {error}")


def listen():
    if sr is None:
        raise RuntimeError(
            f"Speech input is unavailable: {AUDIO_IMPORT_ERROR}. Run the assistant with --text."
        )

    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(
                source,
                timeout=float(os.getenv("ASSISTANT_LISTEN_TIMEOUT", "5")),
                phrase_time_limit=float(os.getenv("ASSISTANT_PHRASE_LIMIT", "15")),
            )
    except sr.WaitTimeoutError:
        return ""
    except (OSError, AttributeError) as error:
        raise RuntimeError(f"Microphone is unavailable: {error}") from error

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.strip().casefold()
    except sr.UnknownValueError:
        print("I could not understand that. Please try again.")
        return ""
    except sr.RequestError as error:
        print(f"Speech recognition service is unavailable: {error}")
        return ""
