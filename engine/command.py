import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.config import ASSISTANT_NAME
import os
from datetime import datetime

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=6)
        except Exception as e:
            eel.DisplayMessage("Error listening.")
            return ""
    try:
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        eel.DisplayMessage(query)
        print(f"User said: {query}")
        time.sleep(1)
        return query.lower()
    except Exception:
        eel.DisplayMessage("Sorry, I couldn't understand.")
        return ""



@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import playYoutube
            playYoutube(query)


        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "search on google" in query or "google" in query:
            from engine.features import GoogleSearch
            GoogleSearch(query)

        elif "search" in query:
            # If "search on google" was already handled above, now handle the rest
            from engine.features import wikiSearch
            wikiSearch(query)




        

        elif "send message" in query or "call" in query or "video call" in query:
            print("Message or call intent detected ✅")
            from engine.features import findContact, whatsApp, makeCall  # remove sendMessage if unused

            contact_no, name = findContact(query)
            print("Resolved contact:", contact_no, name)

            if contact_no != 0:
                speak("Which mode you want to use: WhatsApp or Mobile?")
                preferance = takecommand().lower()
                print("User preferred:", preferance)

                if "mobile" in preferance:
                    if "send message" in query:
                        speak("What message to send?")
                        message = takecommand()
                        print("User message:", message)
                        speak("Mobile SMS not supported. Please use WhatsApp.")
                    elif "call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("I didn't catch that. Please say again.")
                elif "whatsapp" in preferance:
                    if "send message" in query:
                        speak("What message to send?")
                        message = takecommand()
                        whatsApp(contact_no, message, "message", name)
                    elif "call" in query:
                        whatsApp(contact_no, "", "call", name)
                    elif "video call" in query:
                        whatsApp(contact_no, "", "video call", name)
                    else:
                        speak("Please clarify the WhatsApp action.")
            else:
                speak("I could not find that contact.")


        elif "take a screenshot" in query:
            from engine.features import takeScreenshot
            takeScreenshot()


        elif "send email" in query:
            from engine.features import findEmail, send_email

            to_email, name = findEmail(query)  # 🔍 Look up name from DB

            if to_email:
                speak(f"What is the subject of the email to {name}?")
                subject = takecommand()

                speak("What should I say?")
                body = takecommand()

                send_email(to_email, subject, body)  # ✅ Send it!
            else:
                speak("I could not find an email for that contact.")

        elif 'play music' in query:
                        music_dir ='C:\\Users\\kedar\\Music\\Gym'
                        songs = os.listdir(music_dir)
                        print(songs)
                        os.startfile(os.path.join(music_dir,
                        songs[1]))
                        speak("Have a good day Sir...")
        else:
            from engine.features import chatBot
            chatBot(query)

    except Exception as e:
        print("error", e)

    eel.ShowHood()
