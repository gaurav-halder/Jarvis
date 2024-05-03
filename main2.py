import webbrowser
import speech_recognition as sr
import os
from openai import OpenAI
import datetime
import pyperclip
import requests
import json

api_key = ""
wapi_key = '9bfe52920d89fabc6001e7fdeda7c9a8'
content = ""


def say(text, voice='Samantha'):
    os.system(f'say -v {voice} {text}')
# def say(text):
#     os.system(f"say {text}")

def get_location():
    r = requests.get('https://get.geojs.io/')
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    ipAdd = ip_request.json()['ip']

    url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
    geo_request = requests.get(url)
    geo_data = geo_request.json()
    say(f"Sir you are currently in {geo_data['city']} {geo_data['region']} {geo_data['country']}")


def get_weather():

    r = requests.get('https://get.geojs.io/')
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    ipAdd = ip_request.json()['ip']

    url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
    geo_request = requests.get(url)
    geo_data = geo_request.json()
    city = geo_data['city']

    # city = get_location()
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={wapi_key}&units=metric")

    if weather_data.status_code == 404:
        messagebox.showerror("Error", "City not found!")
    else:

        data = weather_data.json()
        temp = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        humidity = round(data['main']['humidity'])

        result_text = f"Sir the Current Temperature is {temp} degree Centigrade but it Feels like {feels_like} degree and the Humidity level is {humidity}"
        say(result_text)

def openAI(query):
    try:
        client = OpenAI(api_key=api_key)
        content = f"Sam: {query}\n Charli(an AI assistant): "

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        print(response)

        say(response["choices"][0]["text"])
        content += f"{response['choices'][0]['text']}\n"

        if "write" in query:
            with open(f"Openai/{''.join(prompt.split('write')[1:]).strip()}.txt", "w") as f:
                f.write(response["choices"][0]["text"])
                pyperclip.copy(response["choices"][0]["text"])

        return response["choices"][0]["text"]


    except Exception as e:
        print(f"An unexpected error occurred")
        print(e)


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio)
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return ""
        except sr.RequestError as e:
            print(f"Request error: {e}")
            return ""

if __name__ == '__main__':

    say("Good morning sir. I m online and ready to assist you .  How can I help you today?")
    while True:
        text = takecommand()

        websites = [["youtube","https://www.youtube.com/"],["google","https://www.google.com/"],["facebook","https://www.facebook.com/"]]
        for site in websites:
            if f"open {site[0]}" in text.lower():
                webbrowser.open(site[1])
        if "play" in text.lower() and "music" in text.lower():
            musicpath = "/Users/snehasishdutta/Downloads/demo.mp3"
            os.system(f"open {musicpath}")
        elif "the" in text.lower() and "time" in text.lower():
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour}  {min} ")
        elif "date" in text.lower():
            today_date = datetime.datetime.now().date()
            say(f"Sir todays date is {today_date}")
        elif "weather" in text.lower() or "temperature" in text.lower():
            get_weather()
        elif "where am i"in text.lower() or "location" in text.lower():
            get_location()
        elif "facetime" in text.lower():
            os.system(f"open /System/Applications/FaceTime.app")
        elif "notion" in text.lower():
            os.system(f"open /Applications/Notion.app")
        elif "quit" in text.lower() or "cut power" in text.lower():
            exit()
        elif "reset chat".lower() in text.lower():
            content = ""
        else:
            if text != "":
                openAI(text.lower())


