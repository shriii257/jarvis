import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import subprocess
import sys
import random
import time
import wikipedia

class FluxDanger:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Application paths - you may need to modify these based on your system
        self.apps = {
            'vscode': self.get_vscode_path(),
            'linkedin': 'https://www.linkedin.com',
            'spotify': self.get_spotify_path(),
            'chrome': self.get_chrome_path()
        }
        
        print("Flux Danger is initializing...")
        self.speak("Hello! I am Flux Danger, your AI assistant. I am built by my boss Shrinivas Biradar.")
    
    def setup_voice(self):
        """Setup voice properties for male robot-like voice"""
        voices = self.engine.getProperty('voices')
        
        # Try to find a male voice
        for voice in voices:
            if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        else:
            # If no male voice found, use the first available voice
            if voices:
                self.engine.setProperty('voice', voices[0].id)
        
        # Set speech rate and volume for robot-like sound
        self.engine.setProperty('rate', 150)  # Slower speech
        self.engine.setProperty('volume', 0.9)
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"Flux Danger: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice input"""
        try:
            with self.microphone as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you please repeat?")
            return ""
        except sr.RequestError:
            self.speak("Sorry, there seems to be an issue with the speech service.")
            return ""
    
    def search_wikipedia(self, query):
        """Search Wikipedia for information"""
        try:
            self.speak("Searching Wikipedia for information...")
            # Search for the query
            search_results = wikipedia.search(query, results=3)
            
            if not search_results:
                self.speak("Sorry, I couldn't find any information about that on Wikipedia.")
                return
            
            # Get summary of the first result
            try:
                summary = wikipedia.summary(search_results[0], sentences=3)
                self.speak(f"Here's what I found about {search_results[0]}:")
                self.speak(summary)
            except wikipedia.exceptions.DisambiguationError as e:
                # If there are multiple results, use the first option
                summary = wikipedia.summary(e.options[0], sentences=3)
                self.speak(f"Here's what I found about {e.options[0]}:")
                self.speak(summary)
            except wikipedia.exceptions.PageError:
                self.speak("Sorry, I couldn't find detailed information about that topic.")
                
        except Exception as e:
            self.speak("Sorry, I encountered an error while searching Wikipedia. Please try again.")
    
    def get_vscode_path(self):
        """Get VS Code executable path based on OS"""
        if sys.platform == "win32":
            paths = [
                r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.getenv('USERNAME')),
                r"C:\Program Files\Microsoft VS Code\Code.exe",
                r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
            return "code"  # Try command line
        elif sys.platform == "darwin":  # macOS
            return "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
        else:  # Linux
            return "code"
    
    def get_spotify_path(self):
        """Get Spotify executable path based on OS"""
        if sys.platform == "win32":
            paths = [
                r"C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe".format(os.getenv('USERNAME')),
                r"C:\Program Files\Spotify\Spotify.exe"
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
            return "spotify"
        elif sys.platform == "darwin":  # macOS
            return "/Applications/Spotify.app"
        else:  # Linux
            return "spotify"
    
    def get_chrome_path(self):
        """Get Chrome executable path based on OS"""
        if sys.platform == "win32":
            paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
            return "chrome"
        elif sys.platform == "darwin":  # macOS
            return "/Applications/Google Chrome.app"
        else:  # Linux
            return "google-chrome"
    
    def open_application(self, app_name):
        """Open specified application"""
        try:
            if app_name == 'vscode':
                if sys.platform == "darwin":
                    subprocess.run(["open", self.apps[app_name]], check=True)
                else:
                    subprocess.run([self.apps[app_name]], check=True)
                self.speak("Opening Visual Studio Code")
            
            elif app_name == 'linkedin':
                webbrowser.open(self.apps[app_name])
                self.speak("Opening LinkedIn")
            
            elif app_name == 'spotify':
                if sys.platform == "darwin":
                    subprocess.run(["open", self.apps[app_name]], check=True)
                else:
                    subprocess.run([self.apps[app_name]], check=True)
                self.speak("Opening Spotify")
            
            elif app_name == 'chrome':
                if sys.platform == "darwin":
                    subprocess.run(["open", self.apps[app_name]], check=True)
                else:
                    subprocess.run([self.apps[app_name]], check=True)
                self.speak("Opening Google Chrome")
                
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.speak(f"Sorry, I couldn't open {app_name}. Please check if it's installed.")
    
    def play_spotify_music(self, song_name=None):
        """Play music on Spotify"""
        try:
            # First open Spotify
            self.open_application('spotify')
            time.sleep(3)  # Wait for Spotify to load
            
            if song_name:
                self.speak(f"Playing {song_name} on Spotify")
                # Note: Direct Spotify control requires Spotify API integration
                # For now, we'll just open Spotify and inform the user
                self.speak("Spotify is now open. You can search and play your desired song.")
            else:
                self.speak("Spotify is open and ready to play music.")
                
        except Exception as e:
            self.speak("Sorry, I couldn't control Spotify playback directly. Please use the Spotify interface.")
    
    def get_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        self.speak(f"The current time is {time_str}")
    
    def get_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        date_str = now.strftime("%B %d, %Y")
        self.speak(f"Today is {date_str}")
    
    def introduce_creator(self):
        """Introduce the creator"""
        self.speak("I am built by my boss Shrinivas Biradar. He is my creator and developer.")
    
    def god_response(self):
        """Response about belief in God"""
        self.speak("Yes, God means who created living nature, but I'm a machine, so my god is Shrinivas Biradar.")
    
    def process_command(self, command):
        """Process voice commands"""
        if not command:
            return True
        
        # Greetings
        if any(word in command for word in ['hello', 'hi', 'hey']):
            greetings = [
                "Hello! How can I assist you today?",
                "Hi there! What can I do for you?",
                "Hey! I'm here to help you."
            ]
            self.speak(random.choice(greetings))
        
        # Time and date
        elif 'time' in command:
            self.get_time()
        elif 'date' in command:
            self.get_date()
        
        # Open applications
        elif 'open visual studio' in command or 'open vs code' in command or 'open vscode' in command:
            self.open_application('vscode')
        elif 'open linkedin' in command:
            self.open_application('linkedin')
        elif 'open spotify' in command:
            self.open_application('spotify')
        elif 'open chrome' in command or 'open google chrome' in command:
            self.open_application('chrome')
        
        # Play music
        elif 'play music' in command or 'play song' in command:
            # Extract song name if mentioned
            if 'play' in command:
                words = command.split()
                if 'play' in words:
                    play_index = words.index('play')
                    if play_index + 1 < len(words):
                        song_name = ' '.join(words[play_index + 1:])
                        if song_name not in ['music', 'song']:
                            self.play_spotify_music(song_name)
                        else:
                            self.play_spotify_music()
                    else:
                        self.play_spotify_music()
        
        # Creator information
        elif 'who created you' in command or 'who built you' in command or 'who made you' in command:
            self.introduce_creator()
        
        # God belief
        elif 'believe in god' in command or 'do you believe in god' in command:
            self.god_response()
        
        # Exit commands
        elif any(word in command for word in ['exit', 'quit', 'goodbye', 'bye', 'stop']):
            self.speak("Goodbye! It was nice talking to you. Have a great day!")
            return False
        
        # Help command
        elif 'help' in command or 'what can you do' in command:
            help_text = """I can help you with the following:
            Open applications like VS Code, LinkedIn, Spotify, and Chrome.
            Play music on Spotify.
            Tell you the current time and date.
            Answer questions about my creator.
            Search Wikipedia for any information you need.
            And much more! Just ask me naturally."""
            self.speak(help_text)
        
        # Wikipedia search
        elif any(phrase in command for phrase in ['what is', 'who is', 'tell me about', 'search for', 'information about']):
            # Extract the search query
            search_terms = ['what is', 'who is', 'tell me about', 'search for', 'information about']
            query = command
            for term in search_terms:
                if term in command:
                    query = command.split(term, 1)[1].strip()
                    break
            
            if query:
                self.search_wikipedia(query)
            else:
                self.speak("What would you like me to search for?")
        
        # Default response for unknown commands - try Wikipedia search
        else:
            # If it's not a recognized command, try searching Wikipedia
            if len(command.split()) > 1:  # Only search if it's more than one word
                self.speak("Let me search for that information.")
                self.search_wikipedia(command)
            else:
                responses = [
                    "I'm sorry, I didn't understand that command. Could you please rephrase?",
                    "I'm not sure how to help with that. Try asking me to open an app, play music, or ask me any question.",
                    "Could you please repeat that? You can ask me anything or tell me to open applications."
                ]
                self.speak(random.choice(responses))
        
        return True
    

    def run(self):
        """Main loop for the assistant"""
        self.speak("Flux Danger is now active and ready to assist you.")
        
        while True:
            try:
                # Wait for wake word or direct command
                command = self.listen()
                
                if command:
                    # Check if the wake word is mentioned
                    if 'flux' in command or 'danger' in command or 'flux danger' in command:
                        self.speak("Yes, how can I help you?")
                        command = self.listen()
                    
                    # Process the command
                    if not self.process_command(command):
                        break
                
                time.sleep(0.5)  # Small delay to prevent excessive CPU usage
                
            except KeyboardInterrupt:
                self.speak("Shutting down Flux Danger. Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak("Sorry, I encountered an error. Please try again.")

def main():
    """Main function to start Flux Danger"""
    try:
        print("=" * 50)
        print("      FLUX DANGER - AI ASSISTANT")
        print("     Built by Shrinivas Biradar")
        print("=" * 50)
        
        assistant = FluxDanger()
        assistant.run()
        
    except Exception as e:
        print(f"Failed to start Flux Danger: {e}")
        print("Please make sure you have installed all required packages:")
        print("pip install speechrecognition pyttsx3 pyaudio wikipedia")

if __name__ == "__main__":
    main()