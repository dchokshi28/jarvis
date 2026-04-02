"""
Jarvis – Voice-controlled personal assistant
=============================================
Wake word: "Jarvis"
After the wake word, speak any command listed below.

Supported commands:
  - Open websites: google, youtube, facebook, linkedin, instagram, twitter,
    github, reddit, stackoverflow, wikipedia, amazon, netflix, spotify,
    whatsapp, chatgpt, gmail
  - Play music: "play <song name>" (from musicLiberary.py or YouTube)
  - Play local music: "play music" (random song from local music folder)
  - Search: "search <query>" / "google <query>"
  - YouTube search: "youtube search <query>"
  - Wikipedia: "wikipedia <topic>" (reads summary aloud)
  - Send email: "send email to <contact>" (predefined contacts)
  - Time: "what time is it" / "time"
  - Date: "what is the date" / "date"
  - App control: "close browser", "close chrome", "stop music", "close notepad"
  - System: "open notepad", "open calculator", "open command prompt"
  - Volume: "volume up", "volume down", "mute"
  - News: "news" / "headlines"
  - Weather: "weather in <city>"
  - Jokes: "tell me a joke" / "joke"
  - Screenshot: "take a screenshot" / "screenshot"
  - IP address: "what is my ip" / "ip address"
  - Stop: "stop" / "exit" / "quit" / "shutdown" / "goodbye"
"""

import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import os
import subprocess
import random
import urllib.parse
import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import musicLiberary

# ── Email configuration ─────────────────────────────────────────────────────
# Update these with your email credentials and contacts
EMAIL_ADDRESS = "your_email@gmail.com"        # ◄── PUT YOUR EMAIL HERE
EMAIL_PASSWORD = "your_app_password"           # ◄── PUT YOUR APP PASSWORD HERE
# For Gmail: generate an App Password at https://myaccount.google.com/apppasswords

# Predefined contacts – say "send email to <name>"
EMAIL_CONTACTS = {
    "example":  "example@gmail.com",
    # Add your contacts below:
    # "john":   "john.doe@gmail.com",
    # "mom":    "mom@email.com",
}

# ── Local music folder ──────────────────────────────────────────────────────
# Set this to your music folder path
MUSIC_DIR = os.path.join(os.path.expanduser("~"), "Music")
MUSIC_EXTENSIONS = (".mp3", ".wav", ".flac", ".aac", ".wma", ".m4a", ".ogg")

# ── TTS Engine ──────────────────────────────────────────────────────────────
# Find the female voice ID once at startup
_engine_temp = pyttsx3.init()
_all_voices = _engine_temp.getProperty("voices")
FEMALE_VOICE_ID = None
for v in _all_voices:
    # On Windows, the female voice is typically "Zira"
    if "zira" in v.name.lower() or "female" in v.name.lower():
        FEMALE_VOICE_ID = v.id
        break
# Fallback: use the second voice if available (usually female on Windows)
if FEMALE_VOICE_ID is None and len(_all_voices) > 1:
    FEMALE_VOICE_ID = _all_voices[1].id
elif FEMALE_VOICE_ID is None:
    FEMALE_VOICE_ID = _all_voices[0].id
_engine_temp.stop()
del _engine_temp


def speak(text):
    """Speak *text* aloud using only the female voice."""
    print(f"Jarvis: {text}")
    engine = pyttsx3.init()
    engine.setProperty("voice", FEMALE_VOICE_ID)
    engine.setProperty("rate", 175)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


# ── Website map ─────────────────────────────────────────────────────────────
WEBSITES = {
    "google":         "https://www.google.com",
    "youtube":        "https://www.youtube.com",
    "facebook":       "https://www.facebook.com",
    "linkedin":       "https://www.linkedin.com",
    "instagram":      "https://www.instagram.com",
    "twitter":        "https://www.twitter.com",
    "github":         "https://www.github.com",
    "reddit":         "https://www.reddit.com",
    "stackoverflow":  "https://stackoverflow.com",
    "stack overflow":  "https://stackoverflow.com",
    "wikipedia":      "https://www.wikipedia.org",
    "amazon":         "https://www.amazon.com",
    "netflix":        "https://www.netflix.com",
    "spotify":        "https://open.spotify.com",
    "whatsapp":       "https://web.whatsapp.com",
    "chatgpt":        "https://chat.openai.com",
    "gmail":          "https://mail.google.com",
    "maps":           "https://maps.google.com",
    "google maps":    "https://maps.google.com",
    "drive":          "https://drive.google.com",
    "google drive":   "https://drive.google.com",
}

# ── Jokes ───────────────────────────────────────────────────────────────────
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
    "There are only 10 types of people in the world: those who understand binary and those who don't.",
    "Why do Java developers wear glasses? Because they can't C#.",
    "A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'",
    "How many programmers does it take to change a light bulb? None. That's a hardware problem.",
    "Why did the developer go broke? Because he used up all his cache.",
    "What's a computer's least favorite food? Spam.",
    "Why did the computer go to the doctor? Because it had a virus!",
    "What do you call a computer that sings? A-Dell.",
]


# ── Command processor ──────────────────────────────────────────────────────
def processCommand(c):
    """Process a single voice command *c*."""
    c_lower = c.lower().strip()

    # ── Open website ────────────────────────────────────────────────────
    if c_lower.startswith("open "):
        site_name = c_lower.replace("open ", "", 1).strip()

        # Check website map first
        if site_name in WEBSITES:
            speak(f"Opening {site_name}")
            webbrowser.open(WEBSITES[site_name])
            return

        # System applications (Windows)
        app_map = {
            "notepad":          "notepad.exe",
            "calculator":       "calc.exe",
            "command prompt":   "cmd.exe",
            "cmd":              "cmd.exe",
            "terminal":         "cmd.exe",
            "paint":            "mspaint.exe",
            "file explorer":    "explorer.exe",
            "explorer":         "explorer.exe",
            "task manager":     "taskmgr.exe",
            "control panel":    "control.exe",
            "settings":         "ms-settings:",
            "word":             "winword.exe",
            "excel":            "excel.exe",
            "powerpoint":       "powerpnt.exe",
        }
        if site_name in app_map:
            speak(f"Opening {site_name}")
            try:
                if site_name == "settings":
                    os.startfile(app_map[site_name])
                else:
                    subprocess.Popen(app_map[site_name])
            except FileNotFoundError:
                speak(f"Sorry, I couldn't find {site_name} on your system.")
            return

        # Fallback: try opening as a URL
        speak(f"Searching for {site_name}")
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(site_name)}")
        return

    # ── Play music ──────────────────────────────────────────────────────
    if c_lower.startswith("play "):
        song = c_lower.replace("play ", "", 1).strip()

        # "play music" → random song from local Music folder
        if song == "music" or song == "a song" or song == "some music":
            try:
                all_songs = []
                for ext in MUSIC_EXTENSIONS:
                    all_songs.extend(glob.glob(os.path.join(MUSIC_DIR, f"**/*{ext}"), recursive=True))
                if all_songs:
                    chosen = random.choice(all_songs)
                    speak(f"Playing {os.path.basename(chosen)}")
                    os.startfile(chosen)
                else:
                    speak(f"No songs found in your Music folder at {MUSIC_DIR}. Playing from YouTube instead.")
                    webbrowser.open("https://www.youtube.com/results?search_query=top+hits+playlist")
            except Exception as e:
                speak(f"Couldn't play local music: {e}")
            return

        # Check music library
        if song in musicLiberary.music:
            speak(f"Playing {song}")
            webbrowser.open(musicLiberary.music[song])
        else:
            # Search on YouTube if not in local library
            speak(f"Searching for {song} on YouTube")
            query = urllib.parse.quote(song)
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return

    # ── Google / web search ─────────────────────────────────────────────
    if c_lower.startswith("search ") or c_lower.startswith("google "):
        query = c_lower.split(" ", 1)[1].strip()
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
        return

    # ── YouTube search ──────────────────────────────────────────────────
    if "youtube search" in c_lower or c_lower.startswith("search youtube for"):
        # Extract the query
        for prefix in ["youtube search ", "search youtube for "]:
            if c_lower.startswith(prefix):
                query = c_lower.replace(prefix, "", 1).strip()
                break
        else:
            query = c_lower.replace("youtube search", "").strip()
        speak(f"Searching YouTube for {query}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
        return

    # ── Wikipedia summary (reads aloud) ─────────────────────────────────
    if c_lower.startswith("wikipedia ") or c_lower.startswith("wiki "):
        query = c_lower.split(" ", 1)[1].strip()
        speak(f"Searching Wikipedia for {query}")
        try:
            import wikipedia
            wikipedia.set_lang("en")
            summary = wikipedia.summary(query, sentences=3)
            print(f"\n📖 Wikipedia: {summary}\n")
            speak(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"There are multiple results. The top one is: {e.options[0]}")
            try:
                summary = wikipedia.summary(e.options[0], sentences=3)
                speak(summary)
            except Exception:
                webbrowser.open(f"https://en.wikipedia.org/wiki/{urllib.parse.quote(query)}")
        except wikipedia.exceptions.PageError:
            speak(f"I couldn't find a Wikipedia page for {query}. Opening search instead.")
            webbrowser.open(f"https://en.wikipedia.org/wiki/Special:Search/{urllib.parse.quote(query)}")
        except Exception as e:
            speak(f"Couldn't fetch Wikipedia summary. Opening the page instead.")
            webbrowser.open(f"https://en.wikipedia.org/wiki/{urllib.parse.quote(query)}")
        return

    # ── Time ────────────────────────────────────────────────────────────
    if "time" in c_lower and ("what" in c_lower or c_lower.strip() == "time"):
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return

    # ── Date ────────────────────────────────────────────────────────────
    if "date" in c_lower and ("what" in c_lower or c_lower.strip() == "date"):
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")
        return

    # ── Day ─────────────────────────────────────────────────────────────
    if "day" in c_lower and "what" in c_lower:
        day = datetime.datetime.now().strftime("%A")
        speak(f"Today is {day}")
        return

    # ── News ────────────────────────────────────────────────────────────
    if c_lower in ("news", "headlines", "latest news", "top news"):
        speak("Opening Google News")
        webbrowser.open("https://news.google.com")
        return

    # ── Weather ─────────────────────────────────────────────────────────
    if "weather" in c_lower:
        city = c_lower.replace("weather", "").replace("in", "").replace("of", "").strip()
        if not city:
            city = "my location"
        speak(f"Showing weather for {city}")
        webbrowser.open(f"https://www.google.com/search?q=weather+{urllib.parse.quote(city)}")
        return

    # ── Joke ────────────────────────────────────────────────────────────
    if "joke" in c_lower:
        joke = random.choice(JOKES)
        speak(joke)
        return

    # ── Screenshot ──────────────────────────────────────────────────────
    if "screenshot" in c_lower:
        try:
            import pyautogui
            screenshot_path = os.path.join(os.path.expanduser("~"), "Desktop", "screenshot.png")
            pyautogui.screenshot(screenshot_path)
            speak(f"Screenshot saved to your Desktop")
        except ImportError:
            speak("Screenshot feature requires pyautogui. Please install it.")
        except Exception as e:
            speak(f"Sorry, couldn't take a screenshot. {e}")
        return

    # ── IP Address ──────────────────────────────────────────────────────
    if "ip address" in c_lower or c_lower == "my ip" or "what is my ip" in c_lower:
        try:
            import socket
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            speak(f"Your local IP address is {ip}")
        except Exception:
            speak("Opening a website to show your public IP")
            webbrowser.open("https://whatismyipaddress.com")
        return

    # ── Volume control (Windows only) ───────────────────────────────────
    if "volume up" in c_lower:
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            new_vol = min(1.0, current + 0.1)
            volume.SetMasterVolumeLevelScalar(new_vol, None)
            speak(f"Volume set to {int(new_vol * 100)} percent")
        except ImportError:
            speak("Volume control requires pycaw. Install it with pip install pycaw.")
        except Exception as e:
            speak(f"Couldn't change volume: {e}")
        return

    if "volume down" in c_lower:
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            new_vol = max(0.0, current - 0.1)
            volume.SetMasterVolumeLevelScalar(new_vol, None)
            speak(f"Volume set to {int(new_vol * 100)} percent")
        except ImportError:
            speak("Volume control requires pycaw. Install it with pip install pycaw.")
        except Exception as e:
            speak(f"Couldn't change volume: {e}")
        return

    if "mute" in c_lower:
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(0.0, None)
            speak("Muted")
        except ImportError:
            speak("Volume control requires pycaw.")
        except Exception as e:
            speak(f"Couldn't mute: {e}")
        return

    # ── How are you ─────────────────────────────────────────────────────
    if "how are you" in c_lower:
        speak("I'm doing great, thank you for asking! How can I help you?")
        return

    # ── Who are you / What is your name ─────────────────────────────────
    if "who are you" in c_lower or "your name" in c_lower:
        speak("I am Jarvis, your personal voice assistant. I'm here to help you!")
        return

    # ── Hello / Hi ──────────────────────────────────────────────────────
    if c_lower in ("hello", "hi", "hey", "good morning", "good afternoon", "good evening"):
        hour = datetime.datetime.now().hour
        if hour < 12:
            speak("Good morning! How can I help you today?")
        elif hour < 17:
            speak("Good afternoon! What can I do for you?")
        else:
            speak("Good evening! How may I assist you?")
        return

    # ── Thank you ───────────────────────────────────────────────────────
    if "thank" in c_lower:
        speak("You're welcome! Always happy to help.")
        return

    # ── Reminder (simple) ──────────────────────────────────────────────
    if c_lower.startswith("remind me to "):
        task = c_lower.replace("remind me to ", "", 1).strip()
        speak(f"I'll remind you to {task}. Note: This is a simple reminder, I've noted it in the console.")
        print(f"[REMINDER] {task}")
        return

    # ── Set a timer (simple) ────────────────────────────────────────────
    if c_lower.startswith("set timer for ") or c_lower.startswith("timer "):
        speak("Timer feature noted. I recommend using your phone's timer for accuracy.")
        return

    # ── Calculate / Math ────────────────────────────────────────────────
    if c_lower.startswith("calculate ") or c_lower.startswith("what is "):
        expression = c_lower.replace("calculate ", "").replace("what is ", "").strip()
        # Sanitize and attempt basic math
        expression = expression.replace("x", "*").replace("×", "*").replace("÷", "/")
        expression = expression.replace("plus", "+").replace("minus", "-")
        expression = expression.replace("times", "*").replace("divided by", "/")
        try:
            # Only allow safe characters
            safe_chars = set("0123456789+-*/.() ")
            if all(ch in safe_chars for ch in expression):
                result = eval(expression)
                speak(f"The answer is {result}")
            else:
                speak(f"Searching for: {c}")
                webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(c)}")
        except Exception:
            speak(f"Searching Google for: {c}")
            webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(c)}")
        return

    # ── Send email ──────────────────────────────────────────────────────
    if "send email" in c_lower or "send mail" in c_lower or "email to" in c_lower:
        speak("Who should I send the email to?")
        # Try to extract contact name from the command itself
        contact_name = None
        for name in EMAIL_CONTACTS:
            if name in c_lower:
                contact_name = name
                break

        if contact_name is None:
            # Listen for the contact name
            try:
                r_email = sr.Recognizer()
                with sr.Microphone() as source:
                    r_email.adjust_for_ambient_noise(source, duration=0.3)
                    audio = r_email.listen(source, timeout=5, phrase_time_limit=5)
                    contact_name = r_email.recognize_google(audio).lower().strip()
            except Exception:
                speak("I couldn't hear the contact name. Please try again.")
                return

        if contact_name not in EMAIL_CONTACTS:
            speak(f"I don't have {contact_name} in my contacts. Please add them to the EMAIL_CONTACTS in main2.py.")
            return

        recipient = EMAIL_CONTACTS[contact_name]

        # Get subject
        speak("What is the subject?")
        try:
            r_email = sr.Recognizer()
            with sr.Microphone() as source:
                r_email.adjust_for_ambient_noise(source, duration=0.3)
                audio = r_email.listen(source, timeout=5, phrase_time_limit=8)
                subject = r_email.recognize_google(audio)
        except Exception:
            speak("I couldn't hear the subject. Sending with default subject.")
            subject = "Message from Jarvis"

        # Get message body
        speak("What should the email say?")
        try:
            r_email = sr.Recognizer()
            with sr.Microphone() as source:
                r_email.adjust_for_ambient_noise(source, duration=0.3)
                audio = r_email.listen(source, timeout=8, phrase_time_limit=15)
                body = r_email.recognize_google(audio)
        except Exception:
            speak("I couldn't hear the message. Please try again.")
            return

        # Send the email
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            speak(f"Email sent successfully to {contact_name}!")
        except smtplib.SMTPAuthenticationError:
            speak("Email authentication failed. Please check your email and app password in the code.")
        except Exception as e:
            speak(f"Failed to send email. Error: {e}")
        return

    # ── Close / app control ─────────────────────────────────────────────
    if c_lower.startswith("close ") or "stop music" in c_lower:
        target = c_lower.replace("close ", "", 1).strip()

        # Map of app names to process names for killing
        close_map = {
            "browser":        ["chrome.exe", "msedge.exe", "firefox.exe", "opera.exe"],
            "chrome":         ["chrome.exe"],
            "google chrome":  ["chrome.exe"],
            "edge":           ["msedge.exe"],
            "firefox":        ["firefox.exe"],
            "notepad":        ["notepad.exe"],
            "calculator":     ["Calculator.exe", "calc.exe"],
            "paint":          ["mspaint.exe"],
            "word":           ["WINWORD.EXE"],
            "excel":          ["EXCEL.EXE"],
            "powerpoint":     ["POWERPNT.EXE"],
            "file explorer":  ["explorer.exe"],
            "task manager":   ["Taskmgr.exe"],
            "vlc":            ["vlc.exe"],
            "spotify":        ["Spotify.exe"],
        }

        # "stop music" → kill common music players
        if "stop music" in c_lower or target == "music":
            music_apps = ["Spotify.exe", "vlc.exe", "wmplayer.exe", "groove.exe",
                          "chrome.exe"]  # Chrome for YouTube music
            speak("Stopping music playback")
            for app in music_apps:
                subprocess.run(["taskkill", "/f", "/im", app],
                               capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            return

        if target in close_map:
            speak(f"Closing {target}")
            for proc in close_map[target]:
                subprocess.run(["taskkill", "/f", "/im", proc],
                               capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            # Try to kill by process name directly
            speak(f"Trying to close {target}")
            subprocess.run(["taskkill", "/f", "/im", f"{target}.exe"],
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return

    # ── Stop / Exit ─────────────────────────────────────────────────────
    if c_lower in ("stop", "exit", "quit", "shutdown", "goodbye", "bye",
                    "go to sleep", "shut down"):
        speak("Goodbye! Have a great day!")
        exit(0)

    # ── Fallback: search Google for anything we don't understand ────────
    speak(f"I'm not sure about that. Let me search for it.")
    webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(c)}")


# ── Main loop ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    # Greet based on time
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning! I'm Jarvis, your personal assistant.")
    elif hour < 17:
        speak("Good afternoon! I'm Jarvis, your personal assistant.")
    else:
        speak("Good evening! I'm Jarvis, your personal assistant.")

    speak("Say 'Jarvis' to wake me up, then tell me what you need.")

    while True:
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                print("\n🎤 Listening for wake word 'Jarvis'...")
                r.adjust_for_ambient_noise(source, duration=0.5)

                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=4)
                except sr.WaitTimeoutError:
                    continue  # Silent – just loop back

            try:
                word = r.recognize_google(audio)
                print(f"Heard: {word}")

                # Check if "jarvis" is in the recognized text
                if "jarvis" in word.lower():
                    speak("Yes? I'm listening.")

                    # Listen for the actual command
                    with sr.Microphone() as source:
                        print("🎤 Listening for command...")
                        r.adjust_for_ambient_noise(source, duration=0.3)
                        try:
                            audio = r.listen(source, timeout=5, phrase_time_limit=8)
                            try:
                                command = r.recognize_google(audio)
                                print(f"Command: {command}")
                                processCommand(command)
                            except sr.UnknownValueError:
                                speak("Sorry, I couldn't understand that. Please try again.")
                            except sr.RequestError:
                                speak("I'm having network issues. Please check your internet.")
                        except sr.WaitTimeoutError:
                            speak("I didn't hear a command. Try again.")

                # Also support compound commands like "Jarvis open Google"
                elif any(word.lower().startswith(f"jarvis {kw}")
                         for kw in ("open", "play", "search", "what", "tell",
                                    "set", "calculate", "remind", "stop",
                                    "weather", "news", "wikipedia", "youtube",
                                    "who", "how", "hello", "hi", "hey",
                                    "volume", "mute", "screenshot", "goodbye",
                                    "close", "send", "email", "wiki")):
                    # Strip "jarvis" prefix and process directly
                    cmd = word.lower().replace("jarvis ", "", 1)
                    processCommand(cmd)

            except sr.UnknownValueError:
                pass  # Didn't catch anything – just loop
            except sr.RequestError as e:
                print(f"Google Speech API error: {e}")
                speak("I'm having trouble connecting. Please check your internet.")

        except OSError as e:
            print(f"Microphone error: {e}")
            speak("I can't access your microphone. Please check it's connected and not in use by another app.")
            import time
            time.sleep(3)
        except KeyboardInterrupt:
            speak("Goodbye!")
            break