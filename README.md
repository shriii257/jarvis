# Flux Danger – Jarvis-Style Desktop Voice Assistant

Flux Danger is a Python-powered personal voice assistant inspired by Marvel’s **Jarvis**.  
It listens to your commands, talks back, opens applications, searches the web, and more—right from your desktop.

---

## ✨ Features
- **Voice Interaction** – Uses [`speech_recognition`](https://pypi.org/project/SpeechRecognition/) to listen and [`pyttsx3`](https://pypi.org/project/pyttsx3/) to speak.
- **Smart Commands**
  - Open apps like **Visual Studio Code**, **Google Chrome**, **Spotify**, and **LinkedIn**.
  - Tell you the current **time** and **date**.
  - Play or launch music on Spotify.
  - Search **Wikipedia** and read a short summary aloud.
- **Wake Word** – Responds when you say “Flux,” “Danger,” or “Flux Danger,” similar to a Jarvis wake word.
- **Cross-Platform** – Handles Windows, macOS, and Linux application paths.

---

## 🛠️ Requirements
- **Python 3.8+**
- Packages:
  ```bash
  pip install speechrecognition pyttsx3 pyaudio wikipedia
