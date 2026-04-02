# 🤖 Jarvis — AI voice Assistant

A Python-based voice-controlled personal assistant for Windows that listens for a wake word and executes a wide range of commands — from opening websites and playing music to sending emails, telling jokes, and controlling system volume.

---

## ✨ Features

| Category | Commands |
|---|---|
| **🌐 Web Browsing** | Open 18+ popular websites (Google, YouTube, GitHub, Reddit, Gmail, etc.) |
| **🎵 Music Playback** | Play songs from a custom library or search YouTube automatically |
| **🔍 Search** | Google search, YouTube search |
| **📖 Wikipedia** | Look up topics and hear summaries read aloud |
| **📧 Email** | Send emails via voice to predefined contacts (Gmail SMTP) |
| **🕐 Date & Time** | Ask for the current time, date, or day |
| **📰 News** | Open Google News for the latest headlines |
| **🌤️ Weather** | Check the weather for any city |
| **😂 Jokes** | Hear a random programmer joke |
| **📸 Screenshot** | Capture and save a screenshot to your Desktop |
| **🌐 IP Address** | Get your local IP address |
| **🔊 Volume Control** | Volume up, volume down, and mute (Windows) |
| **💻 App Control** | Open/close system apps (Notepad, Calculator, Paint, etc.) |
| **🧮 Calculator** | Perform basic math calculations by voice |
| **⏰ Reminders** | Set simple voice reminders (logged to console) |
| **💬 Conversational** | Responds to greetings, "how are you", "who are you", and more |

---

## 📋 Prerequisites

- **Python 3.8+**
- **Windows OS** (uses Windows-specific TTS voices and system commands)
- **Microphone** (for voice input)
- **Internet connection** (for speech recognition via Google API)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Jarvis.git
cd Jarvis
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `PyAudio` may require additional setup on some systems. If `pip install PyAudio` fails, try installing a prebuilt wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) or install via `pipwin`:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 4. Run Jarvis

```bash
python main2.py
```

Jarvis will greet you and start listening for the wake word **"Jarvis"**.

---

## 🗣️ How to Use

1. **Say "Jarvis"** — the assistant will respond with *"Yes? I'm listening."*
2. **Speak your command** — e.g., *"Open YouTube"*, *"Play Shape of You"*, *"What time is it?"*
3. Jarvis processes the command and responds via text-to-speech.

You can also use **compound commands** like *"Jarvis open Google"* in a single phrase.

### Example Commands

```
"Jarvis"  →  "Open YouTube"
"Jarvis"  →  "Play blinding lights"
"Jarvis"  →  "Search Python tutorial"
"Jarvis"  →  "What time is it"
"Jarvis"  →  "Weather in London"
"Jarvis"  →  "Tell me a joke"
"Jarvis"  →  "Take a screenshot"
"Jarvis"  →  "Volume up"
"Jarvis"  →  "Open calculator"
"Jarvis"  →  "Wikipedia artificial intelligence"
"Jarvis"  →  "Send email to John"
"Jarvis"  →  "Goodbye"
```

---

## 📁 Project Structure

```
Jarvis/
├── main2.py            # Main application — wake word listener & command processor
├── musicLiberary.py    # Music library — song name → URL mappings
├── commands.py         # (Reserved for future command extensions)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## ⚙️ Configuration

### 🎵 Music Library

Edit `musicLiberary.py` to add your favorite songs:

```python
music = {
    "shape of you"    : "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "blinding lights" : "https://www.youtube.com/watch?v=4NRXx6U8ABQ",
    # Add more songs here:
    "your song name"  : "https://www.youtube.com/watch?v=YOUR_VIDEO_ID",
}
```

If a song isn't in the library, Jarvis will automatically search YouTube for it.

### 📧 Email Setup

To enable the email feature, update these variables in `main2.py`:

```python
EMAIL_ADDRESS = "your_email@gmail.com"       # Your Gmail address
EMAIL_PASSWORD = "your_app_password"         # Gmail App Password
```

Then add contacts to the `EMAIL_CONTACTS` dictionary:

```python
EMAIL_CONTACTS = {
    "john":  "john.doe@gmail.com",
    "mom":   "mom@email.com",
}
```

> **Important:** Use a [Gmail App Password](https://myaccount.google.com/apppasswords), not your regular password. You must have 2-Step Verification enabled on your Google account.

### 🎶 Local Music Folder

By default, Jarvis looks for local music files in your `~/Music` directory. You can change this in `main2.py`:

```python
MUSIC_DIR = os.path.join(os.path.expanduser("~"), "Music")
```

Supported formats: `.mp3`, `.wav`, `.flac`, `.aac`, `.wma`, `.m4a`, `.ogg`

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `SpeechRecognition` | Converts speech to text via Google Speech API |
| `pyttsx3` | Offline text-to-speech engine |
| `PyAudio` | Microphone audio input |
| `pyautogui` | Screenshot capture |
| `pycaw` | Windows audio/volume control |
| `comtypes` | COM interface support (required by `pycaw`) |

Optional (used if available):
- `wikipedia` — For Wikipedia summary lookups

---

## 🛑 Stopping Jarvis

Say any of the following to exit:

> *"Stop"*, *"Exit"*, *"Quit"*, *"Shutdown"*, *"Goodbye"*, *"Bye"*, *"Go to sleep"*

Or press `Ctrl + C` in the terminal.

---

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| **Microphone not detected** | Ensure your mic is connected and not used by another app |
| **Speech not recognized** | Check your internet connection (Google Speech API requires it) |
| **PyAudio install fails** | Use `pipwin install pyaudio` or download a prebuilt wheel |
| **TTS voice sounds wrong** | Jarvis selects the "Zira" (female) voice on Windows. Install additional voices via Windows Settings → Time & Language → Speech |
| **Email fails** | Verify your Gmail App Password and that 2-Step Verification is enabled |
| **Volume control error** | Ensure `pycaw` and `comtypes` are installed correctly |

---

## 📝 License

This project is open-source and available for personal use and learning purposes.

---

## 🙏 Acknowledgments

- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) — for voice-to-text conversion
- [pyttsx3](https://pypi.org/project/pyttsx3/) — for offline text-to-speech
- [Google Speech API](https://cloud.google.com/speech-to-text) — for cloud-based speech recognition

---

> **Built with ❤️ in Python**
