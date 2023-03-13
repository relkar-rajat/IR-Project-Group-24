
from django.shortcuts import render, redirect
from . import forms
from .models import Details
from .models import Compose
import imaplib,email
from gtts import gTTS
import os
from playsound import playsound
from django.http import HttpResponse
import speech_recognition as sr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.http import JsonResponse
import re

file = "good"
i="0"
passwrd = ""
addr = ""
item =""
subject = ""
body = ""
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
imap_url = 'imap.gmail.com'
conn = imaplib.IMAP4_SSL(imap_url)
attachment_dir = 'C:/Users/Chacko/Desktop/'

def texttospeech(text, filename):
    filename = filename + '.mp3'
    flag = True
    while flag:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            flag = False
        except:
            print('Trying again')
    playsound(filename)
    os.remove(filename)
    return

def speechtotext(duration):
    global i, addr, passwrd
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        playsound('speak.mp3')
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        response = r.recognize_google(audio)
    except:
        response = 'N'
    return response

def convert_special_char(text):
    temp=text
    special_chars = ['attherate','dot','underscore','dollar','hash','star','plus','minus','space','dash']
    for character in special_chars:
        while(True):
            pos=temp.find(character)
            if pos == -1:
                break
            else :
                if character == 'attherate':
                    temp=temp.replace('attherate','@')
                elif character == 'dot':
                    temp=temp.replace('dot','.')
                elif character == 'underscore':
                    temp=temp.replace('underscore','_')
                elif character == 'dollar':
                    temp=temp.replace('dollar','$')
                elif character == 'hash':
                    temp=temp.replace('hash','#')
                elif character == 'star':
                    temp=temp.replace('star','*')
                elif character == 'plus':
                    temp=temp.replace('plus','+')
                elif character == 'minus':
                    temp=temp.replace('minus','-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp=temp.replace('dash','-')
    return temp



def login_view(request):
    global i, addr, passwrd 

    if request.method == 'POST':
        text1 = "Welcome to our Voice Based Email. Login with your email account in order to continue. "
        texttospeech(text1, file + i)
        i = i + str(1)

        flag = True
        while (flag):
            texttospeech("Enter your Email", file + i)
            i = i + str(1)
            addr = speechtotext(10)
            
            if addr != 'N':
                texttospeech("You meant " + addr + " say yes to confirm or no to enter again", file + i)
                i = i + str(1)
                say = speechtotext(3)
                ##############################3
                say='yes'
                if say == 'yes' or say == 'Yes':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
        addr = addr.strip()
        addr = addr.replace(' ', '')
        addr = addr.lower()
        addr = convert_special_char(addr)
        print(addr)
        request.email = addr

        flag = True
        while (flag):
            texttospeech("Enter your password", file + i)
            i = i + str(1)
            passwrd = speechtotext(10)
            
            if addr != 'N':
                texttospeech("You meant " + passwrd + " say yes to confirm or no to enter again", file + i)
                i = i + str(1)
                say = speechtotext(3)
                #############################
                say='yes'
                if say == 'yes' or say == 'Yes':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
        passwrd = passwrd.strip()
        passwrd = passwrd.replace(' ', '')
        passwrd = passwrd.lower()
        passwrd = convert_special_char(passwrd)
        print(passwrd)

        imap_url = 'imap.gmail.com'
        #uncommented password
        passwrd = 'aayxczezuopmutek'
        #addr = ''
        addr='steve8809smith@gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)
        try:
            conn.login(addr, passwrd)
            s.login(addr, passwrd)
            texttospeech("Congratulations. You have logged in successfully. You will now be redirected to the menu page.", file + i)
            i = i + str(1)
            return JsonResponse({'result' : 'success'})
        except:
            texttospeech("Invalid Login Details. Please try again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})

    
    detail  = Details()
    detail.email = addr
    detail.password = passwrd
    return render(request, 'homepage/login.html', {'detail' : detail}) 


