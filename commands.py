import datetime
import os
import shutil
import subprocess
import webbrowser
from urllib.parse import quote_plus

try:
    import psutil
except ImportError:
    psutil = None

WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "instagram": "https://www.instagram.com",
}

APPLICATIONS = {
    "chrome": "chrome.exe" if os.name == "nt" else "google-chrome",
    "vs code": "code",
    "notepad": "notepad.exe" if os.name == "nt" else "gedit",
    "calculator": "calc.exe" if os.name == "nt" else "gnome-calculator",
}


def _open_website(url, label, action="Opening"):
    if not webbrowser.open(url):
        return f"I could not open {label} in your browser."
    return f"{action} {label}"


def _open_application(name):
    executable = APPLICATIONS.get(name)
    if not executable:
        supported = ", ".join(sorted(APPLICATIONS))
        return f"I can only open these apps: {supported}."
    if not shutil.which(executable):
        return f"I could not find {name} on this computer."

    try:
        subprocess.Popen([executable], shell=False)
    except OSError as error:
        return f"I could not open {name}: {error}"
    return f"Opening {name}"


def handle_command(command):
    command = command.casefold().strip()
    if not command:
        return None

    if command in {"help", "what can you do", "available commands"}:
        return (
            "You can ask me questions, ask for the time or date, check battery, "
            "open Google, YouTube or Instagram, open an installed supported app, "
            "search the web, play a YouTube search, or manage memory."
        )

    if command in {"time", "what time is it", "tell me the time"}:
        return f"The current time is {datetime.datetime.now().astimezone().strftime('%H:%M')}."

    if command in {"date", "what is the date", "what's the date", "tell me the date"}:
        return f"Today's date is {datetime.date.today().strftime('%B %d, %Y')}."

    if command in {"battery", "battery status", "what is my battery status"}:
        if psutil is None:
            return "Battery checks require psutil. Install the project requirements first."
        battery = psutil.sensors_battery()
        if battery is None:
            return "Battery information is not available on this computer."
        charging = " and charging" if battery.power_plugged else ""
        return f"Battery is at {battery.percent} percent{charging}."

    if command.startswith("open "):
        name = command.removeprefix("open ").strip()
        if name in WEBSITES:
            return _open_website(WEBSITES[name], name.title())
        return _open_application(name)

    if command.startswith("search for "):
        query = command.removeprefix("search for ").strip()
        if not query:
            return "Tell me what you want to search for."
        return _open_website(
            f"https://www.google.com/search?q={quote_plus(query)}",
            f"Google for {query}",
            "Searching",
        )

    if command.startswith("play "):
        query = command.removeprefix("play ").strip()
        if not query:
            return "Tell me what you want to play."
        return _open_website(
            f"https://www.youtube.com/results?search_query={quote_plus(query)}",
            f"YouTube for {query}",
            "Searching",
        )

    if command in {"shutdown computer", "restart computer"}:
        return "For safety, use your operating system's power menu to shut down or restart."

    return None
