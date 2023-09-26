import datetime
import pyjokes
import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia
import pyautogui  # Import the pyautogui library for simulating key presses

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize recognizer
listener = sr.Recognizer()
with sr.Microphone() as source:
    print('Listening for the wake word...')
    listener.adjust_for_ambient_noise(source)
    listener.dynamic_energy_threshold = True
    listener.energy_threshold = 4000


# Define the wake word
WAKE_WORD = "hey grace"  # Modify the wake word as needed


def talk(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")


def take_command():
    try:
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower()
        if WAKE_WORD in command:
            print('Wake word detected. Listening for a command...')
            talk("Yes, I'm listening. How can I assist you?")
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower().replace(WAKE_WORD, '').strip()
            print(command)

    except sr.RequestError as re:
        print(f"Could not request results from Google Web Speech API: {re}")
    except sr.UnknownValueError:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    return command


def run_grace():
    while True:
        try:
            command = take_command()
            print(command)
            if 'play' in command:
                song = command.replace('play', '').strip()
                if song:
                    talk('Playing ' + song)
                    pywhatkit.playonyt(song)
                else:
                    talk('Please specify a song to play.')
            elif 'time' in command:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                print(current_time)
                talk('The current time is ' + current_time)
            elif any(keyword in command for keyword in ['who is', 'what is', 'read me']):
                query = command.split(' ', 1)[1]
                info = wikipedia.summary(query, 2)
                print(info)
                talk(info)
            elif 'joke' in command:
                talk(pyjokes.get_joke())
            elif 'google' in command:
                query = command.replace('google', '')
                talk('Searching Google for ' + query)
                pywhatkit.search(query)
            elif 'stop' in command:
                talk('Goodbye!')
                break
            elif 'pause' in command:
                # Simulate the spacebar key press to play or pause the media in the browser
                pyautogui.press('space')
            elif 'fast forward' in command or 'ff' in command:
                # Simulate the right arrow key press to fast forward
                pyautogui.press('right')
            elif 'rewind' in command or 'rw' in command:
                # Simulate the left arrow key press to rewind
                pyautogui.press('left')
            elif 'volume up' in command:
                # Simulate the volume up key press
                pyautogui.press('volumeup')
            elif 'volume down' in command:
                # Simulate the volume down key press
                pyautogui.press('volumedown')
            else:
                talk('Please say the command again.')
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    run_grace()
