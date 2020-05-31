import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser as wb
import os
import smtplib
import requests
from pprint import pprint
from selenium import webdriver
from datetime import datetime as dt
import re

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    #speak("Welcome back Harshit")
    hour = int(datetime.datetime.now().hour)
    print(hour)
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    Time = datetime.datetime.now().strftime("%I:%M:%S") 
    print(Time)
    print(date)
    print(month)
    print(year)
    #speak("the current Time is")
    #speak(Time)
    #speak("the current Date is")
    print(custom_strftime('%B {S}, %Y', dt.now()))
    #speak(custom_strftime('%B {S}, %Y', dt.now()))
    #speak(date)
    #speak(month)
    #speak(year)
    if hour>=6 and hour<12:
        speak("Good Morning Harshit!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon Harshit!")

    elif hour>=18 and hour<24:
        speak("Good Evening Harshit!")

    else:
        speak("Good Night Harshit!")

    speak("Gideon, at your Service. Please tell me how can I help You ")
#wishMe()
def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Harshit Said:{query.upper()}\n")
        print(len(query))

    except Exception as e:
        print(e)
        print("Say that again Please...")
        speak("Say that again Please...")
        return "None"
    return query


def lighton():
    driver = webdriver.Chrome('E:\\Project\\Speech recognition\\chromedriver.exe')#add the location of the chrome Drivers
    driver.get("https://Add here.000webhostapp.com/main.html") #Add the webhost name
    elem1 = driver.find_element_by_id("S1off")
    elem1.click()

def lightoff():
    driver = webdriver.Chrome('E:\\Project\\Speech recognition\\chromedriver.exe')
    driver.get("https://Add here.000webhostapp.com/main.html") #Add the webhost name
    elem1 = driver.find_element_by_id("S1on")
    elem1.click()
 

class send_email():
	def __init__(self):
		self.to = ""
		self.content = ""

	def record_message_for_email(self):
		speak("What should I say?")
		self.content = takeCommand()
		speak("message which you want to send is... {}....".format(self.content))
		speak("Do you want to change the message..")
		ans = takeCommand()
		if 'NO' in ans.upper() or 'NOT' in ans.upper() or 'DON''T' in ans.upper() or 'NOPE' in ans.upper():
			return
		else:
			self.record_message_for_email()

	def get_email_content(self):
		try:
			speak("to whom you want to send an email..")
			email = {'RAJ':'harshit20081998@gmail.com','NONE':'1','NEEL':'h7043377227k@gmail.com'}
			to = takeCommand()
			if email.get(to.upper())==None:
				print("Sorry Harshit..{} is not in your contact list".format(to))
				speak("Sorry Harshit..{} is not in your contact list".format(to))
				self.get_email_content()
			elif email.get(to.upper())=='1':
				speak("Sorry harshit, didn't get you,")
				self.get_email_content()
			else:
				self.record_message_for_email()
				speak("Cool Harshit, Sending email to {} Need your confirmation ?".format(to))
				ans = takeCommand()
				if 'YES' in ans.upper() or 'YA' in ans.upper() or 'YEAH' in ans.upper() or 'SURE' in ans.upper() or 'YUP' in ans.upper():
					speak("Okay Harshit... Sending Email to {}".format(to))
					self.to = email[to.upper()]
					self.sendEmail()
					speak("Email has been sent!")
				else:
					speak("Sending email cancelled..")
			    #to = "ReciversEmail@gmail.com"    
		except Exception as e:
				print(e)
				speak("Sorry harshit . I am not able to send this email")

	def sendEmail(self):
	    server = smtplib.SMTP('smtp.gmail.com', 587)
	    server.ehlo()
	    server.starttls()
	    server.login('harshit2772@gmail.com', 'Harshit123')
	    server.sendmail('harshit2772@gmail.com', self.to, self.content)
	    server.close()


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()


        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'search in chrome' in query:
            speak("what should i search?")
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s' #Add the Location of the chrome browser

            r = sr.Recognizer()

            with sr.Microphone() as source:
                print('say something!')
                audio = r.listen(source)
                print("done")
            try:
                text = r.recognize_google(audio)
                print('google think you said:\n' +text +'.com')
                wb.get(chrome_path).open(text+'.com')
            except Exception as e:
                print(e)
        
        elif 'how is the weather' and 'weather' in query:

            url = 'https://api.openweathermap.org/'#Open api link here

            res = requests.get(url)

            data = res.json()

            weather = data['weather'] [0] ['main'] 
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']

            latitude = data['coord']['lat']
            longitude = data['coord']['lon']

            description = data['weather'][0]['description']
            speak('Temperature : {} degree celcius'.format(temp))
            print('Wind Speed : {} m/s'.format(wind_speed))
            print('Latitude : {}'.format(latitude))
            print('Longitude : {}'.format(longitude))
            print('Description : {}'.format(description))
            print('weather is: {} '.format(weather))
            speak('weather is : {} '.format(weather))


        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M:%S")    
            speak(f"Sir, the time is {strTime}")
        
        elif 'the date' in query:
            year = int(datetime.datetime.now().year)
            month = int(datetime.datetime.now().month)
            date = int(datetime.datetime.now().day)
            speak("the current Date is")
            speak(date)
            speak(month)
            speak(year)


        elif 'email to harry' and 'send email' in query:
        	sending_email = send_email()
        	sending_email.get_email_content()
                  

        elif re.search(".*OPEN.*(VS CODE|VISUAL STUDIO CODE).*",query.upper()):
        #elif 'OPEN VISUAL STUDIO CODE' in query.upper() or 'OPEN VS CODE' in query.upper():
        	codePath = "C:\\Users\\Harry\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"#ADD THE PATH OF THE PROGEM HERE
        	os.startfile(codePath)

        elif re.search(".*CLOSE.*(VS CODE|VISUAL STUDIO CODE).*",query.upper()):
        #elif ('CLOSE VS CODE') in query.upper() or 'CLOSE VISUAL STUDIO CODE' in query.upper() or 'CLOSE THE VS CODE' in query.upper() or ('CLOSE THE VISUAL STUDIO CODE')  in query.upper():
        	codePath = "C:\\Users\\Harry\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"#ADD THE PATH OF THE PROGEM HERE
        	result=os.system("taskkill /F /IM Code.exe")
        	if result == 0:
        		print("All nodepads should be death now...")
        	else:
        		print("Error executing taskkill command !!!")

        elif 'open C' in query:
            os.system('explorer C://{}'.format(query.replace('Open','')))

        
        elif 'turn on lights' in query:
            speak("OK,sir turning on the Lights")
            lighton()
            speak("Lights are on")
        
        elif 'turn off lights' in query:
            speak("OK,sir turning off the Lights")
            lightoff()
            speak("Lights are off")



        elif 'goodbye' in query:
            speak("good bye harshit, see you soon.")
            quit()

        
