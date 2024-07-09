import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Faiz: {query}\nJarvis: "
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_message = response["choices"][0]["message"]["content"]
        say(response_message)
        chatStr += f"{response_message}\n"
        return response_message
    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")
        return "Sorry, an error occurred while processing your request."

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_message = response["choices"][0]["message"]["content"]
        text += response_message
    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")
        text += "Sorry, an error occurred while processing your request."

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    filename = f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
    with open(filename, "w") as f:
        f.write(text)

def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-US")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    error_count = 0
    max_errors = 3
    while True:
        query = takeCommand()
        if query:
            error_count = 0  # Reset error count on successful recognition
            sites = [
                ["youtube", "https://www.youtube.com"],
                ["wikipedia", "https://www.wikipedia.com"],
                ["google", "https://www.google.com"]
            ]
            for site in sites:
                if f"open {site[0]}".lower() in query.lower():
                    say(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])

            if "open music" in query.lower():
                musicPath = "/Users/Downloads/Umair - MAKE YOU MINE (Official Audio).mp3"
                os.system(f"open {musicPath}")

            elif "the time" in query.lower():
                hour = datetime.datetime.now().strftime("%H")
                minute = datetime.datetime.now().strftime("%M")
                say(f"Sir, the time is {hour} hours and {minute} minutes.")

            elif "open Zoom" in query.lower():
                os.system(f"open /Users/Zoom/Zoom.exe")

            elif "using artificial intelligence" in query.lower():
                ai(prompt=query)

            elif "jarvis quit" in query.lower():
                exit()

            elif "reset chat" in query.lower():
                chatStr = ""

            else:
                chat(query)
        else:
            error_count += 1
            if error_count >= max_errors:
                print("Too many unsuccessful attempts. Exiting...")
                say("Too many unsuccessful attempts. Exiting...")
                break
