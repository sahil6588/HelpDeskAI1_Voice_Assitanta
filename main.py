import speech_recognition as sr
import os
import webbrowser
import cohere
import datetime
import pywhatkit
import requests
import wikipedia
import pyjokes
import pyautogui
import pyttsx3

# Initialize Cohere
co = cohere.Client("q7OFgUlx90M1UE9JLUb6PNYQVJNxKVNZc2Rz8qiW")

# Initialize pyttsx3 voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)

chatStr = ""

# Speak and print output
def say(text, speak=True):
    print(f"Helpdesk: {text}")
    if speak:
        engine.say(text)
        engine.runAndWait()

# Chat with Cohere using proper chat model
def chat(query):
    global chatStr
    chatStr += f"You: {query}\nHelpdesk: "
    response = co.chat(
        model="command-r",
        message=query,
        temperature=0.7
    )
    result = response.text.strip()
    say(result)
    chatStr += result + "\n"
    return result

# Listen to user command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=30, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.WaitTimeoutError:
            print("Timeout: No voice input received.")
            return ""
        except Exception as e:
            print("Error:", e)
            return ""

# Weather info
def get_weather():
    api_key = "dcc1fc9f6abb95321eaf45af33685ce0"
    city = "Nagpur"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        say(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")
    else:
        say("Sorry, I couldn't fetch the weather.")

# Main program
if __name__ == "__main__":
    say("Hello, How can I help you?")

    while True:
        query = takeCommand().lower()

        if "open" in query:
            if "youtube" in query:
                webbrowser.open("https://youtube.com")
                say("Opening YouTube")
            elif "google" in query:
                webbrowser.open("https://google.com")
                say("Opening Google")
            elif "wikipedia" in query:
                webbrowser.open("https://wikipedia.org")
                say("Opening Wikipedia")

        elif "play music" in query:
            musicPath = "C:\\Users\\YourName\\Music\\song.mp3"
            if os.path.exists(musicPath):
                os.system(f'start "" "{musicPath}"')
                say("Playing your music.")
            else:
                say("Music file not found.")

        elif "time" in query:
            now = datetime.datetime.now()
            say(f"The time is {now.strftime('%H:%M')}")

        elif "reset chat" in query:
            chatStr = ""
            say("Chat history reset.")

        elif "weather" in query:
            get_weather()

        elif "send whatsapp" in query:
            say("Tell me the phone number including country code.")
            number = takeCommand().replace(" ", "")
            say("What is the message?")
            message = takeCommand()
            try:
                pywhatkit.sendwhatmsg_instantly(f"+{number}", message)
                say("Message sent!")
            except:
                say("Failed to send the message. Check the number or internet connection.")

        elif "search google for" in query:
            search_term = query.replace("search google for", "").strip()
            pywhatkit.search(search_term)
            say(f"Searching Google for {search_term}")

        elif "who is" in query or "what is" in query:
            topic = query.replace("who is", "").replace("what is", "").strip()
            try:
                result = wikipedia.summary(topic, sentences=2)
                say(result)
            except:
                say("I couldn't find anything on Wikipedia.")

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            say(joke)

        elif "take a screenshot" in query:
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            say("Screenshot saved.")

        elif "volume up" in query:
            pyautogui.press("volumeup")
            say("Volume increased.")

        elif "volume down" in query:
            pyautogui.press("volumedown")
            say("Volume decreased.")

        elif "shutdown" in query:
            say("Shutting down the system.")
            os.system("shutdown /s /t 1")

        elif "quit" in query or "exit" in query:
            say("Goodbye from Helpdesk")
            break

        else:
            if query.strip():
                chat(query)
            else:
                say("I didn't hear anything.")

