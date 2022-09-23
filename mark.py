import pyttsx3
import speech_recognition as sr
import time
import datetime
from bs4 import BeautifulSoup
from enum import Enum
import pyautogui
import requests
import psutil
import webbrowser
import wikipedia
import os
import random
import socket

# initalizing python text to speech engine
engine = pyttsx3.init()


# speak() function takes the message to speak (recognized by the engine)
def speak(message) :
    engine.say(f'{message}')
    engine.runAndWait()


# voice_input() function recognizes the voice input and returns the text interpreted by the voice recognizer
def voice_input() :

    #Takes voice as input using microphone
    r=sr.Recognizer()
    audio=''

    chunk_size=2048

    with sr.Microphone(chunk_size=chunk_size) as source :
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 500
        audio = r.listen(source,phrase_time_limit=5)

    try :
        print("Recognizing...")
        text=r.recognize_google(audio,language="en-in")
        print(f"User said : {text}\n")
        return text

    except Exception as e :
        print("Unable to Recognize, say that again please...")
        speak("Sorry Sir! I didn't get you. Say that again please..")
        time.sleep(2)
        return 0


# is_internt() tells you that you are connected to internet or not
def is_internet():
    try:
        socket.create_connection(('Google.com',80))
        return True
    except Exception as e:
        print(e)
        return False

# online() function tells user that if connection is established or not
def online():
    
    speak('completing initial checks,')
    speak('please wait a moment sir')
    
    time.sleep(1)
    if is_internet():
        speak('all systems have been started')
        speak('now i am online sir')
        return True
    else:
        speak("can't connect to internet right now")
            
    return False


# wish() function wishes you according to the time at your place
def wish() :
    hour=int(datetime.datetime.now().hour)

    if hour>=0 and hour<12 :
        speak("Good Morning! Sir! ")
    elif hour>=12 and hour<18 :
        speak("Good Afternoon! Sir! ")
    else :
        speak("Good Evening! Sir! ")
    
    speak("I am Mark")



# curr_time() function tells the current time
def curr_time():
    strTime = time.strftime("%I:%M %p")
    speak(f"Time is {strTime}")
    print(strTime)



# curr_date() function tells the current date
def curr_date():
    dat = datetime.datetime.now().date()
    day=time.strftime("%A")
    speak(f"Today's is {day} {dat}")
    print(dat)



# curr_loc() function tells the current location of your device
def curr_loc():
    response = requests.get('https://ipinfo.io/')
    if response.status_code == 200:
        data = response.json()
        city = data['city']
        return city
    else:
        print("Error in the HTTP request")


# curr_temprature() function tells the current temprature in your city
def curr_temprature():   
    #city="temprature of delhi"
    city=f"temprature of {curr_loc()}"
    url=f"https://www.google.com/search?q={city}"

    r=requests.get(url)

    d=BeautifulSoup(r.text,"html.parser")
    temp = d.find("div",class_="BNeawe").text
    speak(f'Current Temperature is {temp}')
    print(f"Temperature: {temp} ")

    lst = []
    lst = temp.split("°")
    return lst[0]



# secs_to_hours() function returns the time in standard time format
def secs_to_hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%dhour, %02d minute, %02s seconds" % (hh, mm, ss)


# global declarations 
greet    = ['hello','hi','whatsup']
userpath = os.environ['USERPROFILE']

class Weather(Enum):
    Hot   = 36
    Humid = 28
    Cold  = 16


# text_processing() function accepts various queries and gives the best possible answers (searches on internet)
# platform independent queires
def text_processing(query):

    if query in greet:
        speak(" At your service Sir")
        return


    elif "who are you" in query or "introduce yourself" in query:
        speak("I am Mark, Your Personal Assistant,"
                " I am here to make your tasks easier. I can help you out by carrying out your various tasks,"
                "such as opening applications,web surfing and many more ")
        return


    elif "who made you" in query or "who created you" in query:
        speak("I developed under the project work of Kailash Bisht")
        return


    elif 'how are you' in query:
        speak("I am fine Sir!")
        speak("What about you?")
        return

    elif 'fine' in query or 'good' in query:
        speak("That's nice Sir")
        return

    elif 'wait' in query or 'hold-on' in query:
        speak("Okay sir! you just finish things off")
        time.sleep(5)
        return

    elif 'thank you' in query or 'thankyou' in query:
        speak('You are Welcome Sir!')
        return


    elif 'what is time' in query :
        speak("Alright, Wait for a moment!")
        curr_time()
        return


    elif 'date today' in query:
        curr_date()
        return


    elif 'day today' in query:
        day=time.strftime("%A")
        speak(f"Today is {day}")
        return


    elif 'weather today' in query or 'current temperature' in query or 'how is the day' in query :
        speak('Weather Report of city Sir!')
        temp = curr_temprature()
        
        if int(temp) > Weather['Hot'].value:
            speak("It's Hot outside!")
            print("Hot Weather")

        elif int(temp) < Weather['Hot'].value and int(temp) > Weather['Humid'].value:
            speak("It's Humid outside!")
            print("Humid Weather")

        elif int(temp) < Weather['Cold'].value:
            speak("It's Cold outside!")
            print("Cold Weather")

        else:
            speak("It's Normal Weather")
            print("Normal Weather")

        return


    elif 'screenshot' in query or 'snapshot' in query:
        speak('Wait a moment Sir!')
        pic     = pyautogui.screenshot()
        timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
        timestr = timestr + ".png"
        desktop = os.path.join(userpath, 'Desktop', timestr)
        pic.save(desktop)
        speak("Ok Sir Done. Check your Desktop")
        return


    elif 'charge remaining' in query or 'battery remaining' in query :
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = int(battery.percent)
        time_left = secs_to_hours(battery.secsleft)
        print(percent)
        if plugged:
            print("don't worry, sir charger is connected, i am charging")
        else:
            if percent < 20:
                print('sir, please connect charger because i can survive only ' + time_left)
            else:
                print('sir, i can survive ' + time_left)


    elif 'wikipedia' in query:
        speak('Searching wikipedia...')
        query=query.replace("wikipedia","")
        results=wikipedia.summary(query,sentences=1)
        speak("According to wikipedia")
        print(results)
        speak(results)
        webbrowser.open_new(f"https://en.wikipedia.org/wiki/{query}")
        speak("Here you can refer to the complete reference.")
        time.sleep(5)
        return
    
    else:
        try:
            speak("OK! I got it")
            webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
            print("Did you mean that!")
            time.sleep(5)
            speak("Hope you are satisfied with results")
            return
        except Exception as e:
            print('Failed! to Load! Incomplete Session ')


# open_webApplication function takes the user query and helps user by opening web applications or searches the user query closely intended by the user
# web applications
def open_webApplication(query):

    if "youtube" in query:
        speak("Alright, Opening YouTube Wait a moment!")
        webbrowser.open_new_tab("https://www.youtube.com/")
        time.sleep(5)
        return


    elif "google" in query:
        speak("Alright, Opening Google in a moment!")
        webbrowser.open_new_tab("https://www.google.com/")
        time.sleep(5)
        return

    elif "instagram" in query:
        speak("Alright, Opening Instagram in a moment!")
        webbrowser.open_new_tab("https://www.instagram.com/")
        time.sleep(5)
        return

    elif "whatsapp" in query:
        speak("Alright, Opening whatsapp in a moment!")
        webbrowser.open_new_tab("https://web.whatsapp.com/")
        time.sleep(5)
        return

    elif "twitter" in query:
        speak("Alright, Opening twitter in a moment!")
        webbrowser.open_new_tab("https://twitter.com/")
        time.sleep(5)
        return

    elif 'github' in query:
        speak('Taking you there Sir!')
        webbrowser.open_new_tab("https://github.com/")
        time.sleep(5)
        return

    elif 'facebook' in query:
        speak('Alright! Opening Facebook in a moment.')
        webbrowser.open_new_tab("https://www.facebook.com/login/")
        time.sleep(5)
        return

    elif 'gmail'in query:
        speak("Alright! Opening Gmail ")
        webbrowser.open_new_tab("https://www.google.com/gmail/")
        time.sleep(5)
        return
    
    else:
        try:
            speak("OK! I got it")
            webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
            print("Did you mean that!")
            time.sleep(5)
            speak("Hope you are satisfied with results")
            return
        except Exception as e:
            print('Failed! to Load! Incomplete Session ')



""" open_application() function contains applications and their path so that the assistant can work with them (windows specific)
one can change the default path of that particular application if they have fixed some other default path"""
# worked with windows applications

def open_application(query):

    if "adobe reader" in query:
        speak("Alright! Opening Adobe Reader, wait a moment")
        default_path_adobe = "C:\\Program Files (x86)\\Adobe\Acrobat Reader DC\\Reader\\AcroRd32.exe"
        os.startfile(default_path_adobe)
        return


    elif "chrome" in query:
        speak("Alright, Opening Google Chrome Wait for a moment!")
        default_path_chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        os.startfile(default_path_chrome)
        return


    elif "mozilla" in query or "firefox" in query:
        speak("Alright, Opening Mozilla Firefox Wait for a moment!")
        default_path_mozilla = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
        os.startfile(default_path_mozilla)
        return


    elif "ms word" in query:
        speak("Alright, Opening Microsoft Word Wait for a moment!")
        default_path_msWord = "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
        os.startfile(default_path_msWord)
        return


    elif 'play music' in query:
        speak("Alright, Playing music in a while !")
        music_dir = "D:\\Pictures\\Songs\\Punjabi"
        song = os.listdir(music_dir)
        res = random.choice(song)
        os.startfile(os.path.join(music_dir, res))
        print(f"Playing \n {res}")
        return


    elif 'vs code' in query:
        speak("Alright, opening VS Code in a while")
        path = "C:\\Users\\Kailash\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(path)
        return

    elif 'pycharm' in query:
        speak("Alright! Opening Pycharm")
        default_path_pycharm = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.1\\bin\\pycharm64.exe"
        os.startfile(default_path_pycharm)
        return

    elif 'python' in query:
        speak("Alright! Opening Python Editor")
        default_path_python = "C:\\Windows\\py.exe"
        os.startfile(default_path_python)
        return


    elif 'my pc' in query:
        speak("Alright, Opening This PC")
        default_path_pc = "C:\\Users\\Kailash\\Desktop\\My PC.lnk"
        os.startfile(default_path_pc)
        return

    elif 'control panel' in query:
        speak("Alright! Opening Control Panel")
        default_path_controlPanel = "C:\\Windows\\System32\\control.exe"
        os.startfile(default_path_controlPanel)
        return

    elif 'run' in query:
        speak("Alright! Wait a moment")
        default_path_run = "C:\\WINDOWS\\system32\\ShellAppRuntime.exe"
        os.startfile(default_path_run)
        return


    elif 'notepad' in query or 'editor' in query:
        speak("Alright, Opening Editor")
        default_notepad_path = ("C:\\Program Files (x86)\\Notepad++\\notepad++.exe")
        os.startfile(default_notepad_path)
        return


    elif 'command prompt' in query or "terminal" in query:
        speak("Alright, opening command prompt in a while")
        linepath = "C:\\WINDOWS\\system32\\cmd.exe"
        os.startfile(linepath)
        return


    elif 'settings' in query:
        speak("Alright! Opening Settings ")
        os.system('start ms-settings:')
        return


    elif 'task manager' in query:
        speak("Alright! Opening Task Manager")
        os.system("start taskmgr")
        return


    elif 'windows media player' in query:
        speak("Alright! Opening Windows Media Player")
        os.system('start wmplayer')
        return


    elif 'paint' in query:
        speak("Alright! Opening Microsoft Paint")
        os.system('start mspaint')
        return


    elif 'environment variables' in query:
        speak('Alright! Opening System Environment Variables Editor')
        os.system('start rundll32.exe sysdm.cpl, EditEnvironmentVariables')
        return


    elif 'device manager' in query:
        speak('Alright! Opening Device Manager')
        os.system('start devmgmt.msc')
        return


    elif 'open store' in query:
        speak('Alright! Opening Windows Store')
        os.system('start ms-windows-store:')
        return


    elif 'calculator' in query:
        speak("Alright! Opening Calculator")
        default_path_calculator = "C:\\Windows\\System32\\calc.exe"
        os.startfile(default_path_calculator)
        return

    else:
        speak("Sorry! Unable to locate")
        print("Please locate the path")
        return


# global declarations

parting = ["bye", "exit", "bye bye", "see you", "okay bye", "okay bye bye", "leave"]

web_applications    = ['google', 'youtube', 'facebook', 'instagram', 'twitter', 'whatsapp', 'gmail', 'github']

system_applications = ['adobe reader', 'chrome', 'mozilla', 'ms word', 'play music', 'vs code', 'pycharm', 'python', 'my pc', 'control panel', 'run', 'notepad', 'command prompt', 'settings', 'task manager', 'windows media player', 'paint', 'environment variables', 'device manager', 'open store', 'calculator']


#response_record() function checks if there is any query missed by the assistant
def response_record():
    recording = sr.Recognizer()

    with sr.Microphone() as source:
        recording.adjust_for_ambient_noise(source)

        print("Listening...")  
        recording.pause_threshold = 1
        recording.energy_threshold = 500 
        audio = recording.listen(source,phrase_time_limit=3)
        
        try:
            text = recording.recognize_google(audio)
            return text
        
        except Exception as e:
            return  0

# system_activation() function wakes-up assistant to take user queries
def system_activation():
    # helps user to give voice imputs

    os.system('cls')
    speak("I am here Sir! Listening...")
    text = voice_input()

    if text != 0:
        text  = text.lower()
                        
        # checks if user wants to leave
        for i in parting:
            if i in text:                   
                speak("Have a good day sir!!")
                print("See you soon")
                exit()
                
        # checks if user want to open applications
        if "open" in text or "play" in text:
            for i in system_applications:
                if i in text:
                    flag = False
                    open_application(i)
                    break
            for i in web_applications:
                if i in text:
                    flag = False
                    open_webApplication(i)
                    break
            
            if flag == True:
                print("Unable to understand")                      
                speak("Can't Open right now")
                        
            time.sleep(2.5)

        else:
            text_processing(text)
            time.sleep(2.5)



# main function or driver code
if __name__=='__main__' :

    os.system('cls')

    if online():
        wish()
        curr_time()
        curr_date()
        curr_temprature()

        while True:
            
            # keeps the assistant always active
            flag = True
            time.sleep(1)
            os.system('cls')

            print("Say 'Hey Mark!' ")
            rec = response_record()

            if rec == 0:
                continue
            
            else:
                system_activation()
                speak("What's next Sir!")

    else:

        print('Connect to internet for better results')

    
        
