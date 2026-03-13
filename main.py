# main.py

import eel
import threading
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
from datetime import datetime
import pytz
import requests
import wikipedia
import pywhatkit
import pyjokes


WEATHER_API_KEY = "985e4cdcfa70c2dd5bd067c251d8f681" 



eel.init('web')


try:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 180)
except Exception as e:
    print(f"TTS Engine initialization failed: {e}")
    engine = None

def speak(text):
    """ Speaks the given text and sends it to the frontend to be displayed. """
    print(f"Assistant: {text}")
    eel.addMessage("Assistant", text)  
    if engine:
        engine.say(text)
        engine.runAndWait()


@eel.expose
def process_command(query):
    """ Main function to process user commands. """
    query = query.lower()

    
    if 'hello' in query or 'hi' in query:
        speak("Hello! How can I assist you today?")
    
 
    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    elif 'open google' in query:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")

    elif 'open mail' in query:
        webbrowser.open("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox")
        speak("Opening Mail.")
    
    elif 'open linkdin' in query:
        webbrowser.open("https://www.linkedin.com/in/amishakale09/")
        speak("Opening linkdin.")

   


    elif 'weather in' in query:
        city = query.split("in")[-1].strip()
        if WEATHER_API_KEY == "YOUR_API_KEY_HERE":
            speak("Weather service is not configured. Please add an API key.")
            return
        base_url = f"http://api.openweathermap.org/data/2.5/weather?appid={WEATHER_API_KEY}&q={city}&units=metric"
        try:
            response = requests.get(base_url).json()
            if response["cod"] != "404":
                main = response["main"]
                desc = response["weather"][0]["description"]
                temp = main["temp"]
                speak(f"The weather in {city} is {desc} with a temperature of {temp}°C.")
            else:
                speak(f"Sorry, I couldn't find the weather for {city}.")
        except Exception:
            speak("Could not connect to the weather service.")
            
    elif 'tell me about' in query or 'who is' in query or 'what is' in query:
        search_term = query.replace("tell me about", "").replace("who is", "").replace("what is", "").strip()
        try:
            result = wikipedia.summary(search_term, sentences=2)
            speak(f"According to Wikipedia: {result}")
        except Exception:
            speak(f"Sorry, I couldn't find any information on {search_term}.")

  
    elif 'play' in query and 'on youtube' in query:
        song = query.replace('play', '').replace('on youtube', '').strip()
        speak(f"Playing {song} on YouTube.")
        pywhatkit.playonyt(song)
    elif 'tell me a joke' in query:
        speak(pyjokes.get_joke())
    

    elif 'exit' in query or 'goodbye' in query or 'quit' in query:
        speak("Goodbye! Have a great day.")
        
        eel.closeWindow()
        
    else:
        speak("I'm not sure how to help with that. Can you try another command?")


if __name__ == "__main__":
    
  eel.start('index.html', mode='chrome', size=(700, 600), cmdline_args=['--disable-http-cache'])
   
   