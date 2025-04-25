import os
import eel
from datetime import datetime

from engine.features import *
from engine.command import *
from engine.auth import recoganize
def start():
    
    eel.init("www")

    playAssistantSound()
    @eel.expose
    def init():
        # subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()


            def wishMe():
                hour = int(datetime.now().hour)
                tm = datetime.now().strftime("%H:%M:%S")
                if 3 <= hour < 12:
                    speak("Good Morning Sir!")
                elif 12 <= hour < 18:
                    speak("Good Afternoon Sir!")
                else:
                    speak("Good Evening Sir!")
                speak(f" it's {tm}, I am Ultron...Tell me, how can I help you")

            wishMe()


            # speak("Hello, Welcome Sir, How can i Help You")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Fail")
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)