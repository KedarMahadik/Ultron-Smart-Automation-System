import os
from urllib.parse import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from datetime import datetime
from playsound import playsound
import eel
import pyaudio
import pyautogui
import pywhatkit as kit
import pvporcupine
from hugchat import hugchat
import pywhatkit as pwk

from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term, remove_words
from engine.command import speak, takecommand

con = sqlite3.connect("ultron.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

# Open apps or websites
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()

    app_name = query.strip()

    if app_name != "":
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + app_name)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening " + app_name)
                    webbrowser.open(results[0][0])
                else:
                    speak("Opening " + app_name)
                    try:
                        os.system('start ' + app_name)
                    except:
                        speak("not found")
        except:
            speak("something went wrong")

# Play YouTube
# def PlayYoutube(query):
#     search_term = extract_yt_term(query)
#     speak("Playing " + search_term + " on YouTube")
#     kit.playonyt(search_term)

    # for custom searching
def playYoutube(query):
    speak("what should i play")
    pl = takecommand().lower() # type: ignore
    pwk.playonyt(f"{pl}")

# def GoogleSearch(query):
#     speak("Welcome sir... Opening Google for you.")
#     speak("Sir, what should I search on Google?")
                
#     search_query = takecommand().lower()  # Get the search query from user's voice input
#     search_url = f"https://www.google.com/search?q={search_query}"
                
#     webbrowser.open(search_url)  # Open the Google search results page in the default web browser

import webbrowser
from urllib.parse import quote
from engine.features import speak, takecommand  # Adjust import based on your file structure

def GoogleSearch(query):
    """Handle custom Google search from voice input."""
    try:
        speak("What should I search for?")
        search_query = takecommand().lower()

        if search_query.strip() == "":
            speak("Sorry, I didn't catch that. Please try again.")
            return

        url = f"https://www.google.com/search?q={quote(search_query)}"
        webbrowser.open(url)
        speak(f"Here are the results for {search_query} on Google.")
        print(f"Opened Google search for: {search_query}")

    except Exception as e:
        speak("Something went wrong while trying to search on Google.")
        print("Google search error:", e)

    
import wikipedia
import webbrowser
from engine.command import speak, takecommand

def wikiSearch(query=None):
    try:
        if not query or query.strip() == "":
            speak("What topic do you want me to search on Wikipedia?")
            query = takecommand()
        
        speak(f"Searching Wikipedia for {query}...")
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia...")
        speak(result)
        print("Wikipedia Summary:", result)

    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple results. Opening browser for more info.")
        url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        webbrowser.open(url)

    except wikipedia.exceptions.PageError:
        speak("I couldn't find anything on Wikipedia. Let me search on the web.")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    except Exception as e:
        speak("Something went wrong. Opening Google as backup.")
        webbrowser.open(f"https://www.google.com/search?q={query}")



# Hotword detection using Porcupine
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["ultron", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("hotword detected")
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# Find contacts
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", 
                       ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print("Contact search result:", results)

        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    

    # --------------------------1st working code for opening only-----------
# def whatsApp(mobile_no, message, flag, name):
#         if not mobile_no.startswith("+"):
#             mobile_no = "+91" + mobile_no

#         encoded_message = quote(message.strip()) if message else ""

#         if flag == 'message':
#             speak(f"Sending WhatsApp message to {name}")
#             url = f"https://wa.me/{mobile_no}?text={encoded_message}"
#         elif flag == 'call':
#             speak(f"Opening WhatsApp chat with {name} for call")
#             url = f"https://wa.me/{mobile_no}"
#         elif flag == 'video call':
#             speak("Opening chat, video call must be initiated manually.")
#             url = f"https://wa.me/{mobile_no}"
#         else:
#             speak("Unknown WhatsApp action requested.")
#             return

#         try:
#             webbrowser.open(url)
#             time.sleep(3)
#         except Exception as e:
#             speak("Failed to open WhatsApp Web.")
#             print("WhatsApp Web error:", e)




import pywhatkit as kit

# def whatsApp(mobile_no, message, flag, name):
#     if not mobile_no.startswith("+"):
#         mobile_no = "+91" + mobile_no

#     if flag == 'message':
#         speak(f"Sending WhatsApp message to {name}")
#         try:
#             kit.sendwhatmsg_instantly(
#                 phone_no=mobile_no,
#                 message=message,
#                 wait_time=10,
#                 tab_close=True,
#                 close_time=3
#             )
#             speak(f"Message sent successfully to {name}")
#         except Exception as e:
#             speak("Failed to send WhatsApp message.")
#             print("Error:", e)

#     elif flag == 'call' or flag == 'video call':
#         speak(f"Opening WhatsApp chat with {name}. Please initiate the call manually.")
#         url = f"https://wa.me/{mobile_no}"
#         try:
#             webbrowser.open(url)
#         except Exception as e:
#             speak("Failed to open WhatsApp Web.")
#             print("WhatsApp Web error:", e)


# -@@@@@@@@@@@@@@@@@@@@@@@@-------working automatic message sending-------@@@@@@@@@@@@@@@@@@@@@-------------


def whatsApp(mobile_no, message, flag, name):
    if not mobile_no.startswith("+"):
        mobile_no = "+91" + mobile_no
    if flag == 'message':
        speak(f"Sending WhatsApp message to {name}")
        try:
            kit.sendwhatmsg_instantly(mobile_no, message, wait_time=10, tab_close=True, close_time=3)
            speak(f"Message sent successfully to {name}")
        except Exception as e:
            speak("Failed to send WhatsApp message.")
            print("Error:", e)
    else:
        speak(f"Opening WhatsApp chat with {name}. Please initiate the call manually.")
        webbrowser.open(f"https://wa.me/{mobile_no}")




# ---------------------1st working code for calling with manual only----------------
# def makeCall(name, mobile_no):
#     from urllib.parse import quote

#     if not mobile_no.startswith('+'):
#         mobile_no = '+91' + mobile_no  # You can customize country code here

#     try:
#         speak(f"Opening WhatsApp Web to call {name}")
#         print(f"Simulating WhatsApp call to {name} at {mobile_no}")

#         # Open WhatsApp Web with the person's chat
#         url = f"https://wa.me/{quote(mobile_no)}"
#         webbrowser.open(url)

#         speak("Please click the call icon manually on WhatsApp Web.")
#         eel.DisplayMessage("🔔 WhatsApp Web chat opened. You can place the call manually.")
#     except Exception as e:
#         print("Error opening WhatsApp Web:", e)
#         speak("Unable to open WhatsApp Web.")


def makeCall(name, mobile_no):
    if not mobile_no.startswith('+'):
        mobile_no = '+91' + mobile_no

    speak(f"Do you want to make a voice call or video call to {name}?")
    call_type = takecommand().lower()

    try:
        if "video" in call_type:
            speak(f"Opening WhatsApp Web chat with {name} for video call")
        else:
            speak(f"Opening WhatsApp Web chat with {name} for voice call")

        url = f"https://wa.me/{mobile_no}"
        webbrowser.open(url)

        speak("Please click the call icon manually on WhatsApp Web.")
        eel.DisplayMessage("🔔 WhatsApp Web chat opened. Click the 📞 or 🎥 icon to initiate the call.")
    except Exception as e:
        speak("Unable to open WhatsApp Web.")
        print("Call Error:", e)


# ChatBot
def takeScreenshot():
    # Create folder if it doesn't exist
    folder = "screenshots"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(folder, f"screenshot_{timestamp}.png")

    # Take screenshot and save
    image = pyautogui.screenshot()
    image.save(filepath)

    speak(f"Screenshot taken successfully and saved in screenshots folder ")
    eel.DisplayMessage("📸 Screenshot saved.")



# ---------------------------------------- Video and Audio Recording -----------------------------

#1st working code









def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# Note: makeCall and sendMessage are still using ADB and would need to be updated if full web-based control is needed.




#for custom email 
def findEmail(query):
    from engine.helper import remove_words

    words_to_remove = [ASSISTANT_NAME, "send", "email", "to"]
    query = remove_words(query, words_to_remove).strip().lower()

    try:
        cursor.execute("SELECT email FROM contacts WHERE LOWER(name) LIKE ?", ('%' + query + '%',))
        results = cursor.fetchall()
        if results:
            return results[0][0], query
        else:
            speak("No email found for that contact.")
            return None, None
    except Exception as e:
        speak("Error retrieving email.")
        print("findEmail error:", e)
        return None, None


import smtplib
from email.message import EmailMessage
from engine.config import Password, Email
def send_email(to_email, subject, body):
    try:
        sender_email = Email  # ----@*&%----
        sender_password = Password  # ----@*&%----

        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        speak(f"Email sent successfully to {to_email}")
    except Exception as e:
        speak("Failed to send the email.")
        print("Email Error:", e)



import cv2
import numpy as np
import pyttsx3
import threading
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Dummy Image and Video file paths for simulation
IMAGE_PATH = 'sample_image.jpg'
VIDEO_PATH = 'sample_video.mp4'

# Simulating photo capture
def capture_photo():
    print("Simulating photo capture...")
    # Load a predefined image (simulate capturing)
    img = cv2.imread(IMAGE_PATH)
    
    if img is not None:
        cv2.imwrite('captured_image.jpg', img)
        pyttsx3.speak("Photo captured successfully.")
    else:
        pyttsx3.speak("Failed to capture photo. No camera detected.")
        print("Error: Image not found!")

# Simulating zoom functionality (we'll use image resizing as an example)
def zoom_in():
    print("Simulating zoom-in...")
    img = cv2.imread(IMAGE_PATH)
    if img is not None:
        height, width = img.shape[:2]
        zoomed_img = cv2.resize(img, (int(width * 1.2), int(height * 1.2)))
        cv2.imwrite('zoomed_in_image.jpg', zoomed_img)
        pyttsx3.speak("Zoomed in successfully.")
    else:
        pyttsx3.speak("No image to zoom in.")

def zoom_out():
    print("Simulating zoom-out...")
    img = cv2.imread(IMAGE_PATH)
    if img is not None:
        height, width = img.shape[:2]
        zoomed_out_img = cv2.resize(img, (int(width * 0.8), int(height * 0.8)))
        cv2.imwrite('zoomed_out_image.jpg', zoomed_out_img)
        pyttsx3.speak("Zoomed out successfully.")
    else:
        pyttsx3.speak("No image to zoom out.")

# Simulating a filter change (for simplicity, just apply a simple effect)
def next_filter():
    print("Simulating filter change...")
    img = cv2.imread(IMAGE_PATH)
    if img is not None:
        # Apply a simple effect: converting to grayscale (as a filter)
        filtered_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('filtered_image.jpg', filtered_img)
        pyttsx3.speak("Filter applied successfully.")
    else:
        pyttsx3.speak("No image to apply filter.")

# Simulating video recording start (just a placeholder message)
def record_start():
    print("Simulating video recording start...")
    pyttsx3.speak("Video recording started.")
    
    # Simulate video recording by just playing a predefined video file
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        pyttsx3.speak("Failed to open video file.")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Display video frame (not required for actual recording in simulation)
        cv2.imshow('Simulated Video Recording', frame)
        
        # Break loop if 'q' is pressed (to simulate recording stop)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    pyttsx3.speak("Video recording stopped.")

# Simulating voice commands and threading for background listening
def listen_for_commands():
    # This would normally listen to voice, but here we're simulating it.
    # The simulation simply runs the commands one by one.
    print("Simulating voice command listening...")
    
    commands = [
        "capture photo",
        "zoom in",
        "zoom out",
        "change filter",
        "start recording"
    ]
    
    for command in commands:
        print(f"Simulated Command: {command}")
        handle_command(command)
        time.sleep(2)  # Wait between commands

# Handle simulated commands
def handle_command(command):
    if "capture" in command:
        capture_photo()
    elif "zoom in" in command:
        zoom_in()
    elif "zoom out" in command:
        zoom_out()
    elif "change filter" in command:
        next_filter()
    elif "start recording" in command:
        record_start()
    else:
        print("Command not recognized.")

# Main function to simulate the process
def main():
    # Start the listening for commands in a background thread
    listening_thread = threading.Thread(target=listen_for_commands)
    listening_thread.start()
    
    # Simulate a delay for the commands to process
    listening_thread.join()

# Call main function to simulate the process
if __name__ == "__main__":
    main()



