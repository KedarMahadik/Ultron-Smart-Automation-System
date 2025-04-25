import pyttsx3 # type: ignore
import speech_recognition as sr # type: ignore
import wikipedia # type: ignore
import webbrowser
import os
from datetime import datetime
import cv2 # type: ignore
from requests import get # type: ignore
import pywhatkit as pwk # type: ignore
import sys
import pyjokes # type: ignore

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


    
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',
voices[len(voices)-1].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
def wishMe():
    hour = int(datetime.now().hour)
    tm = datetime.now().strftime("%H:%M:%S")
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening")
    speak(f" Sir, it's {tm}, I am NOVA...Tell me, how can I help you")

wishMe()

def takeCommand():
# it takes microphone input from user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
    # after giving command by user jarvis
    # will take time of 1 sec to reply
        audio = r.listen(source, timeout = 10, phrase_time_limit=8)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language = 'en-in')
        print(f"User said:{query}\n")
    except Exception as e:
        # print(e)
            print("Say that again please...")
            return "None"
    return query

def send_email(receiver_email, subject, body):
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        sender_email = 'dravidiangaming143@gmail.com'
        password = 'divyeshwarade'
        smtp_server.login(sender_email, password)
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
            
        smtp_server.send_message(message)
        smtp_server.quit()




import pywhatkit as pwk # type: ignore
import pyautogui # type: ignore

def send_whatsapp_message(phone_number, message, time_hour, time_minute):
    pwk.sendwhatmsg(f"+{phone_number}", message, time_hour, time_minute)

import pyautogui # type: ignore
direction = 0
def minimize_window():
                pyautogui.hotkey('win', 'm')

def maximize_window():
                pyautogui.hotkey('win', 'up')

def close_tab():
                pyautogui.hotkey('ctrl', 'w')

def switch_tab(direction='right'):
        speak("ok...wait")


if __name__ == "__main__":

 
   
    while True:
        query = takeCommand().lower()
        


        if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia","")
                results = wikipedia.summary(query,
                sentences=5)
                speak("According to Wikipedia")
                print(results)
                speak(results)
        #---------------------------->>>>>>>>here nova must give info about user spoken thing
        

        
        elif direction == 'right':
                        pyautogui.hotkey('ctrl', 'tab')
        elif direction == 'left':
                        pyautogui.hotkey('ctrl', 'shift', 'tab')

        elif 'minimise window' in query:
                        minimize_window()
                        speak("Window minimized successfully!")

        elif 'maximize the window' in query:
                        maximize_window()
                        speak("Window maximized successfully!")

        elif 'close tab' in query:
                        close_tab()
                        speak("Tab closed successfully!")

        elif 'switch tab' in query:
                if 'right' in query:
                                switch_tab(direction='right')
                                speak("Switched to the next tab.")
                elif 'left' in query:
                        switch_tab(direction='left')
                        speak("Switched to the previous tab.")

        
        elif 'open google' in query:
                        speak("Welcome sir... Opening Google for you.")
                        
                        # Extract the search query from the user's command
                        search_query = query.replace('open google and search for', '').strip()
                        
                        if search_query:
                                # Construct the Google search URL with the query
                                search_url = f"https://www.google.com/search?q={search_query}"
                                
                                # Open the Google search results page in the default web browser
                                webbrowser.open(search_url)
                        else:
                                speak("Sir, what should I search on Google?")
                                search_query = takeCommand().lower()  # Get the search query from user's voice input
                                if search_query:
                                        search_url = f"https://www.google.com/search?q={search_query}"
                                        webbrowser.open(search_url)
                                else:
                                        speak("Sorry, I couldn't understand your query.")
        elif 'search on google' in query:
                
                speak("Welcome sir... Opening Google for you.")
                speak("Sir, what should I search on Google?")
                
                search_query = takeCommand().lower()  # Get the search query from user's voice input
                search_url = f"https://www.google.com/search?q={search_query}"
                
                webbrowser.open(search_url)  # Open the Google search results page in the default web browser


        elif 'send whatsapp message' in query:
                        phone_number = "9850718871"  
                
                        speak("Tell me your message!")
                        message = takeCommand().lower()  
                        time_hour = 17
                        time_minute = 11
                        send_whatsapp_message(phone_number, message, time_hour, time_minute)
                        

        elif 'click photo' in query:
                        def capture_photo(camera_index=0, photo_path="captured_photo.jpg"):
                        # Initialize the camera
                                cap = cv2.VideoCapture(camera_index)
                
                                
                                if not cap.isOpened():
                                        print("Error: Unable to open camera.")
                                        return
                                
                                # Capture a frame
                                ret, frame = cap.read()
                                
                                if not ret:
                                        print("Error: Unable to capture frame.")
                                        return
                                
                                # Write the captured frame to a file
                                cv2.imwrite(photo_path, frame)
                                
                                # Release the camera
                                
                                speak("Say!,cheese!")
                                print("Photo captured successfully!")
                                # cap.release()
                        
                                cap.release()

                        if __name__ == "__main__":
                                capture_photo()


        elif 'open stackoverflow' in query:
                        webbrowser.open('stackoverflow.com')#-------------..........
                        # .................................>>>>jarvis
                        # must open stackoverflow
        elif 'open linkedin' in query:
                        webbrowser.open("Linkedin.com")
                        speak("sure")
        elif 'open geeksforgeeks' in query:
                        webbrowser.open('geeksforgeeks.com')
                        # elif 'open chat Gpt' in query:
                        # webbrowser.openI("chat.openai.com/auth/login?next=%2F")
        elif 'how are you' in query:
                        speak("I am fine sir...what about you")
        elif 'project teacher' in query:
                        speak("sinu mam")
                        

        # elif 'open Notepad' in query:
        #                 os.startfile("C:\ProgramData\Microsoft\Windows\StartMenu\Programs\Accessories.exe")
                
        elif 'play music' in query:
                        music_dir ='C:\\Users\\kedar\\Music\\Favorite songs'
                        songs = os.listdir(music_dir)
                        print(songs)
                        os.startfile(os.path.join(music_dir,
                        songs[1]))
                        speak("Have a good day Sir...")
                
                        
        elif 'open code' in query:
                        codePath ="C:\\Users\\kedar\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                        os.startfile(codePath)
                
        elif 'open calculator' in query:
                        webbrowser.open("calculator")
        elif 'open facebook' in query:
                        webbrowser.open("Facebook.com")
                        
        elif 'open command prompt' in query:
                        path1 ="C:\\Users\\kedar\\AppData\\Roaming\\Microsoft\\Windows\\StartMenu\\Programs\\System Tools\\CommandPrompt.lnk"
                        os.startfile(path1)
                        # to close the cmd
        elif 'close command prompt' in query:
                        speak("ok sir, command promt is closing")
                        os.system("taskkill /f /im Command Prompt.lnk")
                
        elif "tell me a joke" in query:
                        joke = pyjokes.get_joke()
                        speak(joke)

                        
        elif "shutdown the system" in query:
                        os.system("shutdown /s /t 5")
        elif "restart the window" in query:
                        os.system("shutdown /r /t 5")
        elif "sleep the system" in query:
                        os.system("rundll32.exepowrprof.dll,SetSuspendState 0,1,0")
                
                
        elif "ip address" in query:
                        ip = get('http://api.ipify.org').text
                        speak(f"your ip address is {ip}")
                
        elif "open youtube" in query:
                        speak("what should i play")
                        pl = takeCommand().lower() # type: ignore
                        pwk.playonyt(f"{pl}")
                
        # elif "open whatsapp" in query:
        #                 phone_number = "7720032922"  # Replace with recipient's phone number
        #                 message = "Hello, this is a test message!"  # Replace with your message
        #                 send_whatsapp_message(phone_number, message)
        elif "close the system" in query:
                        speak("System is now closing...have a good day sir")
                        sys.exit()  
        elif 'hey nova' in query:
                        speak("Hello Sir, Is there anything for me!!!!!!!")


        elif "send email" in query:
                        speak("What should I write in the email?")
                        email_body = takeCommand().lower() # Assuming the body is dictated
                        receiver_email = 'kedarmahadik528@gmail.com' # Enter recipient's email address
                        subject = 'Subject of the email' # Enter the subject
                        send_email(receiver_email, subject, email_body)
                        speak("Email has been sent successfully!")


                
        elif 'send me email' in query:
                        import speech_recognition as sr # type: ignore
                        import yagmail # type: ignore

                        recognizer=sr.Recognizer()
                        with sr.Microphone() as source:
                                print("Clearing background noise...")
                                recognizer.adjust_for_ambient_noise(source,duration=1)
                                speak("what message you want to send")
                                print("Waiting for your message...")
                                recordedaudio=recognizer.listen(source)
                                print('Done recording...!')

                        try:
                                speak('Printing the message...')
                                text=recognizer.recognize_google(recordedaudio,language='en-US')

                                print('Your message:{}' .format(text))
                                

                        except Exception as ex:
                                print(ex)

                        receiver='kedarmahadik21@gmail.com'
                        message = text
                        sender = yagmail.SMTP('godkdgift@gmail.com')
                        sender.send(to=receiver,subject='This is an automated mail',contents=message)
                        speak("message send successfully")

