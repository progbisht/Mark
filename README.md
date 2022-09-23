# Mark
Mark is a voice assistant that can open you system application, search over internet, open web applications, play music and search on wikipedia.
It is not a learning based agent but logical statements working with python text to speech engine and google speech recognition API.
It can only work when the internet connection is enabled as the speech recognition can work only with the internet connection.

# Setup 
Python version 3.6.x or later
Python packages required - pyttsx3, 
                           speech_recognition, 
                           time, 
                           datetime, 
                           BeautifulSoup, 
                           Enum, 
                           pyautogui, 
                           requests, 
                           psutil, 
                           webbrowser, 
                           wikipedia, 
                           os, 
                           random, 
                           socket
All the above mentioned packages need to be installed.   

# How to run 
Click on the executable file inside dist directory. A prompt will start. You need internet connection for the assistant to respond.
Once the assistant will detect internet connection it will automaticaly introduce itself. 
It continiously detects the voice input and you are required to wake-up the assistant every time for every query by saying 'Hey Mark' and then,
you can pose your queries once it says 'I am here Sir' and displays 'Listening....'.

Assistant can take queries for 5 secs once it displays 'Listening...' and then waits for the next 1 sec to go again.

# Demo
S-1 : As soon as it displays the current time, date and temprature it starts recognizing voices and displays 'Say Hey Mark!'. 

S-2 : Next you have to say 'Hey Mark' when it displays 'Listening...' and then the assistant says 'I am here Sir Listening...'.

S-3 : Once it displays 'Listening'  you can pose queries like 'open google' or 'open youtube' or 'open command prompt' or 'best hotels in shimla' etc.

Repeat S-2 and S-3 to work with assistant.

Once user says 'bye' or 'leave' in query or any keyword in 'parting list' the assistant will finish its execution.

For more you can refer to the working images of the model.
