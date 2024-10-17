import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib

print("Initializing Kiki Voice Assisantant")
MASTER = "Mugesh Rao"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    print(hour)

    if hour >= 0 and hour < 12:
        speak("good morning" + MASTER)

    elif hour >= 12 and hour < 18:
        speak("good afternoon" + MASTER)

    else:
        speak("good Evening" + MASTER)

    speak("i am your Assisant . How may I help you?")


def sendemail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('mugeshraoego@gmail.ocm', 'password')
    server.sendmail("harry@gmail.com", to, content)
    server.close()


# This function will take command from the microphone
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        query = None

    return query


# main program starting
def main():
    speak("Initializing Kiki Voice Assissant...")
    wishme()
    query = takecommand()

    # Logic for executing tasks as per the query
    if 'wikipedia' in query.lower():
        speak('searching wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        print(results)
        speak(results)

    elif 'open youtube' in query.lower():
        webbrowser.open('youtube.com')
        url = "youtube.com"
        chrome_path = 'c:/program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif 'open google' in query.lower():
        webbrowser.open('youtube.com')
        url = "google.com"
        chrome_path = 'c:/program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif 'play music' in query.lower():
        songs_dir = "C:\\Users\\Dell\\Desktop\\Photos\\audio"
        songs = os.listdir(songs_dir)
        print(songs)
        os.startfile(os.path.join(songs_dir, songs[0]))

    elif 'the time' in query.lower():
        strtime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"{MASTER} the time is {strtime}")

    elif 'open code' in query.lower():
        codepath = "C:\\Users\\Dell\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codepath)

    elif 'email to raj' in query.lower():
        try:
            speak("what should i send")
            content = takecommand()
            to = "harry@gmail.com"
            sendemail(to, content)
            speak("Email has been sent to raj")
        except Exception as e:
            print(e)


main()