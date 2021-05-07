from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import Audio1Form
from .models import Audio1doc
import csv
import boto3
import json
import time
import speech_recognition as sr

# Create your views here.

def home(request):
    return render(request,'Git_App/home.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'Git_App/login.html', {'form':AuthenticationForm()})
    else:
        uname = request.POST['username']
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'Git_App/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('dashboard')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'Git_App/signup.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                username=request.POST['username'] 
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                return render(request,'Git_App/message.html',{'username':username})
            except IntegrityError:
                return render(request, 'Git_App/signup.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'Git_App/signup.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return render(request,'Git_App/logoutmessage.html')

def dashboard(request):
    return render(request,'Git_App/dashboard.html')

def import_doc_csv(request):
    if request.method =='POST':
        csv_file = request.FILES['csv_file']
        file_data=csv_file.read().decode("utf-8")
        lines=file_data.split("\n")
        print(lines)
        content_list=""
        for line in lines:
            try:
                content_list= content_list + str(line)
            except:
                print("Finish")
        print(content_list)
        aws_con_man=boto3.session.Session(profile_name="default")
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        print('Calling DetectSentiment')
        result=comprehend.detect_sentiment(Text=content_list, LanguageCode='en')
        endresult=[]
        endresult=result["Sentiment"]
        print('End of DetectSentiment\n')
    return render(request,'Git_App/dashboard.html',{ 'endresult' : endresult })

def analysis(request):
    if request.method == 'POST' :
        text=request.POST['test']
        aws_con_man=boto3.session.Session(profile_name="default")
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        print('Calling DetectSentiment')
        result=comprehend.detect_sentiment(Text=text, LanguageCode='en')
        result1=result["Sentiment"]
        print('End of DetectSentiment\n')
    return render(request,'Git_App/dashboard.html',{ 'result1' : result1 })

def Audioupload(request):
    if request.method == 'POST':  
        form = Audio1Form(request.POST, request.FILES)
        na=request.POST['Name']
        if form.is_valid():
            form.save()
        fil=""
        for e in Audio1doc.objects.all():
            if e.Name == na :
                fil=e.Action
                print(fil)
        r=sr.Recognizer()
        with sr.AudioFile(fil) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = r.listen(source)
            text=r.recognize_google(audio_data)
            print(text)
        return render(request,'Git_App/text.html', { 'text' : text })
    else:
        form = Audio1Form()
        return render(request, 'Git_App/sent.html', {'form' : form})

def test(request):
    if request.method == 'POST':
        audiofile= request.FILES['filetest']
        r=sr.Recognizer()
        with sr.AudioFile(audiofile) as source:
            audio_data = r.record(source)
            text=r.recognize_google(audio_data)
            print(text)
    return render(request, 'Git_App/text.html', {'text' : text})



