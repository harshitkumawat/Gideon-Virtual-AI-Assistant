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
import subprocess
import json
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

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
    Time = datetime.datetime.now().strftime("%I:%M:%S") 
    print(Time)
    #speak("the current Time is")
    #speak(Time)
    #speak("the current Date is")
    print(custom_strftime('%B {S}, %Y', dt.now()))
    #speak(custom_strftime('%B {S}, %Y', dt.now()))
    if hour>=4 and hour<12:
        speak("Good Morning Harshit!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon Harshit!")

    elif hour>=18 and hour<22:
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

    except Exception as e:
        print(e)
        print("Say that again Please...")
        speak("Say that again Please...")
        return "None"
    return query
 
#================================================================================#
# Created Class send_email to Ask Gideon to get content and Send Email.    		 #
# Author : Harshit Kumawat														 #
#================================================================================# 
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
			email = {'RAJ':'harshit20081998@gmail.com','NONE':'1','NEEL':'h7043377227k@gmail.com','DEEPU':'diplata.kumawat55@gmail.com','HAPPY':'hemlata.kumawat7@gmail.com'}
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
	    server.login('********@gmail.com', '**********')
	    server.sendmail('harshit2772@gmail.com', self.to, self.content)
	    server.close()
#================================================================================#
# End																			 #
#================================================================================# 

#================================================================================#
# Created class to Ask Gideon to open windows application						 #
# Author : Harshit Kumawat														 #
#================================================================================# 
class open_close_application():
	def __init__(self):
		pass

    # Function to open Vs Code
	def OPEN_VS_CODE(self):
		codePath = "C:\\Users\\Harry\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"#ADD THE PATH OF THE PROGEM HERE
		subprocess.Popen(codePath)
		speak("Okay Harshit.. opening Visual Studio Code.")

	# Function to Close Vs Code	
	def CLOSE_VS_CODE(self):
		result=os.system("taskkill /F /IM Code.exe")
		speak("Okay Harshit.. Closing Visual Studio Code.")
		if result == 0:
			print("All VS code should be death now...")
		else:
			print("Error executing taskkill command !!!")

	# Function to Open Calculator
	def OPEN_Calculator(self):
		subprocess.Popen('C:\\Windows\\System32\\calc.exe')
		speak("Okay Harshit.. opening Calculator.")

	# Function to Close Calculator	
	def CLOSE_Calculator(self):
		result=os.system("taskkill /F /IM calculator.exe")
		speak("Okay Harshit.. Closing Calculator.")
		if result == 0:
			print("All Calculator should be death now...")
		else:
			print("Error executing taskkill command !!!")

	def OPEN_Word(self):
		speak('Okay harshit. opening Microsoft Word.')
		os.system('start winword')

	# Function to Close Vs Code	
	def CLOSE_Word(self):
		speak('Okay harshit. closing Microsoft Word.')
		result=os.system("taskkill /F /IM winword.exe")
		if result == 0:
			print("All Word files should be death now...")
		else:
			print("Error executing taskkill command !!!")

    # Function to open drive
	def search_drive(self):
		speak("Can you please tell me in which drive you want to search  ?")
		drive = takeCommand()
		if re.search(".*(E DRIVE|EDRIVE|D DRIVE|DDRIVE|C DRIVE|CDRIVE|SEA DRIVE|SEE DRIVE).*",drive.upper()):
			if re.search(".*(E DRIVE|EDRIVE).*",drive.upper()):
				speak("Yes harshit i am in E Drive..")
				self.search_file_folder('E:')
			elif re.search(".*(D DRIVE|DDRIVE|THE DRIVE).*",drive.upper()):
				speak("Yes harshit i am in D Drive..")
				self.search_file_folder('D:')
			elif re.search(".*(C DRIVE|CDRIVE).*",drive.upper()):
				speak("Yes harshit i am in C Drive..")
				self.search_file_folder('C:')
		elif re.search(".*(CANCEL|DON'T|NO|LEAVE).*",drive.upper()) and drive.upper()!="NONE":
			speak("Okay Harshit Cancelling the search..")
		else:
			speak("I didn't get you..")
			self.search_drive()

				
    # Function to search file and folder in drive      
	def search_file_folder(self,drive):
		speak("What should i search? a File or a Folder ?")
		arr = os.listdir(drive+'/')
		ans = takeCommand()
		if re.search(".*(FILE|5|FILES).*",ans.upper()):
			files = [i for i in arr if os.path.isfile(drive+'/'+i)]
			if len(files)!=0:
				speak("okay Harshit.. here is the list {}".format(files))
			else:
				speak("No files present in this drive")
				self.search_file_folder(drive)
		elif re.search(".*(FOLDER|FOLDERS).*",ans.upper()):
			folders = [i for i in arr if os.path.isdir(drive+'/'+i)]
			if len(folders)!=0:
				speak("list of folders are {}".format(folders))
			else:
				speak("No folders present in this folder")
				self.search_file_folder(drive)
		elif re.search(".*(GO BACK|GO TO PREVIOUS|MOVE BACK|MOVE TO PREVIOUS).*",ans.upper()):
			speak("Going Back to Drive list..")
			self.search_drive()
		elif re.search(".*(CANCEL|DON'T|NO|LEAVE).*",ans.upper()) and ans.upper()!="NONE":
			speak("Okay Harshit Cancelling the search..")
		else:
			speak("I didn't get you..")
			self.search_file_folder(drive)

#================================================================================#
# End                                                                            #
#================================================================================# 

#================================================================================#
# Class to get Weather  report from openweathermap                               #
#================================================================================# 

class get_weather_report_from_openweathermap():
        def __init__(self):
            self.api_key = "6dad8caa267eb523c37470c8f23621c6"
            self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
            self.city_name = "Surat"
        # Function to get Weather details
        def get_weather_report(self,query):
            get_city = query.upper().split()
            try:
                idx = get_city.index('IN') or get_city.index('OF')
                self.city_name = get_city[idx+1]
            except:
                self.city_name = "Surat"
            complete_url = self.base_url + "appid=" + self.api_key + "&q=" + self.city_name 
            res = requests.get(complete_url)
            print(res)
            data = res.json()
            print(data)
            weather = data['weather'] [0] ['main'] 
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            latitude = data['coord']['lat']
            longitude = data['coord']['lon']
            description = data['weather'][0]['description']
            speak("Current Weather in {}".format(self.city_name))
            speak('Temperature : {0:.2f} degree celcius'.format(int(temp)-273.15))
            print('Wind Speed : {0:.2f} m/s'.format(wind_speed))
            print('Latitude : {}'.format(latitude))
            print('Longitude : {}'.format(longitude))
            print('Description : {}'.format(description))
            print('weather is: {} '.format(weather))
            speak('weather is : {} '.format(weather))
            speak("Harshit, do you want detailed weather report ?")
            while True:
                detailed_ans = takeCommand()
                if re.search("(YES|SURE|OFCOURSE|WHY NOT)",detailed_ans.upper()) and detailed_ans.upper()!="NONE":
                    speak("Okay, here is the detailed report..")
                    speak('Temperature : {0:.2f} degree celcius'.format(int(temp)-273.15))
                    speak('weather is : {} '.format(weather))
                    speak("Wind Speed : {0:.2f} kilometer per hour".format(wind_speed*(18/5)))
                    speak("Latitude : {}".format(latitude))
                    speak("Longitude : {}".format(longitude))
                    speak("Description : {}".format(description))
                elif re.search("(NO|DON'T)",detailed_ans.upper()) and detailed_ans.upper()!="NONE":
                    speak("Okay harshit..Tell me what else i can do for you?")
                    return
                else:
                    speak("I didn't get you?")
                    speak("Harshit, do you want detailed weather report ?")
                
#================================================================================#
# End                                                                            #
#================================================================================# 

#================================================================================#
# Class to Get file from Google Drive Using API                                  #
#================================================================================# 
class Google_Drive_API():
    def __init__(self):
        credentials_file_path = './credentials/credentials.json'
        clientsecret_file_path = './credentials/client_secret.json'
        # define API scope
        SCOPE = 'https://www.googleapis.com/auth/drive'
        # define store
        store = file.Storage(credentials_file_path)
        credentials = store.get()
        # get access token
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(clientsecret_file_path, SCOPE)
            credentials = tools.run_flow(flow, store)
        self.http = credentials.authorize(Http())
        self.drive = discovery.build('drive', 'v3', http=self.http)
    def retrieve_all_files(self,api_service):
        results = []
        page_token = None

        while True:
            try:
                param = {}

                if page_token:
                    param['pageToken'] = page_token

                files = api_service.files().list(**param).execute()
                # append the files from the current result page to our list
                results.extend(files.get('files'))
                # Google Drive API shows our files in multiple pages when the number of files exceed 100
                page_token = files.get('nextPageToken')

                if not page_token:
                    break

            except errors.HttpError as error:
                print(f'An error has occurred: {error}')
                speak("An error has occurred {}".format(error))
                break

        return results

    def list_(self,file_to_list,type_of_file):
        if len(file_to_list)!=0:
            speak("Okay Harshit. Their are {} {} in your Drive..".format(len(file_to_list),type_of_file))
            while True:
                speak("Should i list all files?")
                ans = takeCommand()
                if re.search("(YES|SURE|WHY NOT|YUP|YEAH)",ans.upper()) and ans.upper()!="NONE":
                    speak("Cool, Here is the list. {}".format(file_to_list))
                elif re.search("(NO|LEAVE|DON'T|IT'S FINE|IT'S OK)",ans.upper()) and ans.upper()!="NONE":
                    speak("Okay no problem.")
                    return
                else:
                    speak("Sorry, I didn't get you")
        else:
            speak("Sorry harshit, their is no {} in your Drive..".format(type_of_file))


    def Search_File(self):
        speak("getting info from your google drive...")
        all_files = self.retrieve_all_files(self.drive)
        speak("Okay Harshit. Their are {} files and folders in your Drive..".format(len(all_files)))
        while True:
            speak("What should i search file or folder?")
            file_or_folder = takeCommand()
            if 'FILE' in file_or_folder.upper():
                speak("Okay! Which file?")
                filename_to_search = takeCommand()
                if re.search("WORD",filename_to_search.upper()):
                    word = []
                    for file in all_files:
                        if 'word' in file.get('mimeType'):
                            word.append(file.get('name'))
                    self.list_(word,'Word File')

                elif re.search("PDF",filename_to_search.upper()):
                    pdf = []
                    for file in all_files:
                        if 'pdf' in file.get('mimeType'):
                            pdf.append(file.get('name'))
                    self.list_(pdf,'pdf')

                elif re.search("(IMAGES|IMAGE|PICTURES|PICTURE)",filename_to_search.upper()):
                    image = []
                    for file in all_files:
                        if 'image' in file.get('mimeType'):
                            image.append(file.get('name'))
                    self.list_(image,'Image')
            elif 'FOLDER' in file_or_folder.upper():
                folder = []
                for file in all_files:
                    if 'folder' in file.get('mimeType'):
                        folder.append(file.get('name'))
                self.list_(folder,'Folder')
            elif re.search("(NO|LEAVE|DON'T|IT'S FINE|IT'S OK|NOTHING)",file_or_folder.upper()) and file_or_folder.upper()!="NONE":
                speak("Okay no problem. What else i can do ?")
                return
            else:
                speak("Sorry, I didn't get you")



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
                print('google think you said:\n' +text)
                wb.get(chrome_path).open(text)
            except Exception as e:
                print(e)
        
        elif re.search("(WEATHER)",query.upper()):
            weather_report = get_weather_report_from_openweathermap()
            weather_report.get_weather_report(query) 

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

#================================================================================#
# Ask Gideon to Send Email														 #
# Author : Harshit Kumawat														 #
#================================================================================# 
        elif 'email to harry' and 'send email' in query:
        	sending_email = send_email()
        	sending_email.get_email_content()
#================================================================================#
# End																			 #
#================================================================================# 

#================================================================================#
# Ask Gideon to Open Mail App                                                    #
# Author : Harshit Kumawat                                                       #
#================================================================================# 
        elif re.search("(MAIL APP|OPEN MAIL APP|OPEN MAIL)",query.upper()):
            #open_Mail = open_close_applications()
            #open_Mail.Open_Mail_App()
            speak("Opening Mail App..")
            os.system('start outlookmail:')
             # Function to close Mail App
#================================================================================#
# Ask Gideon to Close Mail App                                                   #
#================================================================================# 
        elif re.search("(CLOSE MAIL APP|CLOSE MAIL)",query.upper()):
            #close_Mail = open_close_applications()
            #closeMail.Close_Mail_App()
            speak('Okay harshit. closing Mail App.')
            result=os.system("taskkill /F /IM HxOutlook.exe")
            if result == 0:
                print("All Mail App should be death now...")
            else:
                print("Error executing taskkill command !!!")
#================================================================================#
# End                                                                            #
#================================================================================# 

#================================================================================#
# Ask Gideon to Open Camera                                                      #
# Author : Harshit Kumawat                                                       #
#================================================================================# 
        elif re.search("(CLICK.*PICTURE|OPEN.*CAMERA|ON.*WEB CAMERA|ON.*WEB CAM)",query.upper()):
            speak("Switching on the Web Cam..")
            os.system('start microsoft.windows.camera:')
#================================================================================#
#  Ask Gideon to Close Camera                                                    #
#================================================================================# 
        elif re.search("(CLOSE.*CAMERA|OFF.*WEB CAMERA|OFF.*WEB CAM)",query.upper()):
            speak("Switching off the Web Cam..")
            result=os.system("taskkill /F /IM  WindowsCamera.exe")
            if result == 0:
                print("All Cameras should be death now...")
            else:
                print("Error executing taskkill command !!!") 
#================================================================================#
# End                                                                            #
#================================================================================#            

#================================================================================#
# Ask Gideon to Open Visual Studio Code 										 #
# Author : Harshit Kumawat														 #
#================================================================================# 
        elif re.search(".*OPEN.*(VS CODE|VISUAL STUDIO CODE).*",query.upper()):
        	open_vs_code = open_close_application()
        	open_vs_code.OPEN_VS_CODE()
#================================================================================#
# End																			 #
#================================================================================# 

#================================================================================#
# Ask Gideon to Close Visual Studio Code 										 #
# Author : Harshit Kumawat														 #
#================================================================================# 
        elif re.search(".*CLOSE.*(VS CODE|VISUAL STUDIO CODE).*",query.upper()):
        	close_vs_code = open_close_application()
        	close_vs_code.CLOSE_VS_CODE()
#================================================================================#
# End																			 #
#================================================================================# 

#================================================================================#
# Ask Gideon to Calculator  													 #
# Author : Harshit Kumawat														 #
#================================================================================# 
        elif re.search(".*OPEN.*(CALCI|CALCULATOR).*",query.upper()):
        	Calculator = open_close_application()
        	Calculator.OPEN_Calculator()
#================================================================================#
# End																			 #
#================================================================================# 

#================================================================================#
# Ask Gideon to Calculator 														 #
# Author : Harshit Kumawat														 #
#================================================================================# 
        elif re.search(".*CLOSE.*(CALCI|CALCULATOR).*",query.upper()):
        	Calculator.CLOSE_Calculator()
#================================================================================#
# End																			 #
#================================================================================# 

#================================================================================#
# Ask Gideon to open new word document 											 #
# Author : Harshit Kumawat														 #
#================================================================================# 
        elif re.search(".*OPEN.*(WORD|DOCUMENT).*",query.upper()):
        	word = open_close_application()
        	word.OPEN_Word()
#================================================================================#
# End																			 #
#================================================================================# 

#================================================================================#
# Ask Gideon to Close word document												 #
# Author : Harshit Kumawat														 #
#================================================================================# 
        elif re.search(".*CLOSE.*(WORD|DOCUMENT).*",query.upper()):
        	word.CLOSE_Word()
#================================================================================#
# End																			 #
#================================================================================# 

#================================================================================#
# Ask Gideon to search file in Google Drive                                      #
# Author : Harshit Kumawat                                                       #
#================================================================================# 
        elif re.search("(GOOGLE DRIVE|SEARCH.*GOOGLE DRIVE|DRIVE)",query.upper()):
            google_drive_search = Google_Drive_API()
            google_drive_search.Search_File()


#================================================================================#
# End                                                                            #
#================================================================================# 
#================================================================================#
# Ask Gideon to search file														 #
# Author : Harshit Kumawat														 #
#================================================================================# 
        elif re.search("SEARCH.*(FILE|FOLDER)",query.upper()):
        	search = open_close_application()
        	search.search_drive()
#================================================================================#
# End																			 #
#================================================================================# 
        elif 'goodbye' in query:
            speak("good bye harshit, see you soon.")
            quit()

        
