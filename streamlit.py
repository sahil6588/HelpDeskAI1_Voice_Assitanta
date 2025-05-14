import streamlit as st
import cohere
import requests
import wikipedia
import pyjokes
import datetime

# Cohere setup
co = cohere.Client("q7OFgUlx90M1UE9JLUb6PNYQVJNxKVNZc2Rz8qiW")

# Weather config
api_key = "dcc1fc9f6abb95321eaf45af33685ce0"
city = "Nagpur"

st.set_page_config(page_title="Helpdesk AI", layout="centered")

# Session state to remember chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""

st.title(" Helpdesk AI Assistant")

# User Input
user_input = st.text_input("Ask your question here ", "")

# Functions
def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {desc}."
    else:
        return "Sorry, I couldn't fetch the weather."

def generate_response(query):
    st.session_state.chat_history += f"You: {query}\nHelpdesk: "
    response = co.chat(
        message=query,
        temperature=0.7
    )
    answer = response.text.strip()
    st.session_state.chat_history += answer + "\n"
    return answer

# When the user asks something
if user_input:
    if "weather" in user_input:
        response = get_weather()
    elif "joke" in user_input:
        response = pyjokes.get_joke()
    elif "time" in user_input:
        now = datetime.datetime.now()
        response = f"The current time is {now.strftime('%H:%M')}"
    elif "who is" in user_input or "what is" in user_input:
        try:
            topic = user_input.replace("who is", "").replace("what is", "").strip()
            response = wikipedia.summary(topic, sentences=2)
        except:
            response = "I couldn't find anything on Wikipedia."
    else:
        response = generate_response(user_input)

    st.markdown(f"** You:** {user_input}")
    st.markdown(f"** Helpdesk:** {response}")

st.markdown("---")
st.text_area("Chat History", st.session_state.chat_history, height=300)
