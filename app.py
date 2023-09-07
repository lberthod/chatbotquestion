#-*- mode: python -*-
# -*- coding: utf-8 -*-
 # loic.berthod@hevs.ch /lberthod@gmail.com
 # python script : openai chatgpt 3-5, whister, pyttsx3, ai text to speak
 # do the pip install you need
 # pip install sounddevice soundfile numpy openai colorama pydub fpdf pyttsx3 langchain pyrebase
 # need to have a chatbot.txt et openaiapikey.txt
 # -*- coding: utf-8 -*-
import streamlit as st
from gtts import gTTS

import sounddevice as sd
import soundfile as sf
import numpy as np
import openai
import os
import requests
import re
from colorama import Fore, Style, init
import datetime
import base64
from pydub import AudioSegment
from pydub.playback import play
import time
import string
from fpdf import FPDF
 
import pyttsx4
import pyrebase

 # ceci est les import langchain pour gerer la gestion avec les prompts et memoire
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool

import pyrebase
from elevenlabs import generate, play

from elevenlabs import set_api_key
import pyrebase

config = {
    "apiKey": "AIzaSyAZ9NNn6W2WOX3JY5-tswLX8fm9OOfH7Z0",
  "authDomain": "chatbotsoloia.firebaseapp.com",
  "databaseURL": "https://chatbotsoloia-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "chatbotsoloia",
  "storageBucket": "chatbotsoloia.appspot.com",
  "messagingSenderId": "305385169995",
  "appId": "1:305385169995:web:2adb0ef70c1dd310a159ce",
  "measurementId": "G-Y15MRTZ33Z"
}
engine = pyttsx4.init()
apis = st.secrets["elevenlabs"]

set_api_key(apis)
os.environ['OPENAI_API_KEY'] = st.secrets["auth"]
 


rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate
voices = engine.getProperty('voices')

volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[38].id)   #changing index, changes voices. 1 for female

 
init()
# Typical Non-streaming request
start_time = time.time()

 
config = {
    "apiKey": "AIzaSyAZ9NNn6W2WOX3JY5-tswLX8fm9OOfH7Z0",
    "authDomain": "chatbotsoloia.firebaseapp.com",
    "projectId": "chatbotsoloia",
    "databaseURL": "https://chatbotsoloia-default-rtdb.europe-west1.firebasedatabase.app/",
    "storageBucket": "chatbotsoloia.appspot.com",
    "messagingSenderId": "305385169995",
    "appId": "1:305385169995:web:2adb0ef70c1dd310a159ce",
    "measurementId": "G-Y15MRTZ33Z"
}
 
firebase = pyrebase.initialize_app(config)
db = firebase.database()
 
 
# Prompt templates
question1a_template = PromptTemplate(
    input_variables = ['question1'], 
    template="Instructions : Vous allez recevoir un message.  Votre tâche consiste à de redonner uniquement si le retour est Oui ou Non.    Sans information complémentaire, juste le mot Oui ou Non Voici le retour du questionnaire : {question1}")



# Memory 
question1_memory = ConversationBufferMemory(input_key='question1', memory_key='question1_memory')
 
# Llms
llm = OpenAI(temperature=0.9) 
question1a_chain = LLMChain(llm=llm, prompt=question1a_template, verbose=True, output_key='question1a_output', memory=question1_memory)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
 
def val():
    val = val + 1 
    return val
def incrementer_compteur():
    # On définit une variable compteur qui gardera sa valeur entre les appels à la fonction grâce au mot-clé 'Nonlocal'.
    # Si la variable n'existe pas encore, elle est créée avec une valeur de 0.
    global compteur
    compteur += 1  # On incrémente le compteur de 1 à chaque passage.
    return compteur
 
# On initialise le compteur à 0 avant d'appeler la fonction.
compteur = 0
api_key = "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"

def speak1(text1):
    test = text1
    
    audio = generate(
    text=test,
    voice="Arnold",
    model='eleven_multilingual_v1'
    )   

    play(audio)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    engine.stop()

 
def addDialogue1(message):
    valeur_finale = incrementer_compteur()
    information = "Kevin : " + message
    data = {valeur_finale: information}
 #   db.child("Dialogue").child("1").set(data)
    db.child("Dialogue").child("1").update(data)
 
    return ""
 
 
def record_and_transcribe(fs=44100):
    print('Recording...')
    val1 = 5
    myrecording = sd.rec(int(val1 * fs), samplerate=fs, channels=1)
    sd.wait()
    print('Recording complete.')
    filename = 'myrecording.wav'
    sf.write(filename, myrecording, fs)
    with open(filename, "rb") as file:
        openai.api_key = api_key
        result = openai.Audio.transcribe("whisper-1", file)
    transcription = result['text']
    print(transcription)
    return transcription

db = firebase.database()
def addData(message, retour):
    
    data = {"question": message , "reponse":retour}
    datas = {message : data}
    print("a : " + message)
 #   db.child("Dialogue").child("1").set(data)
    db.child("question").child("idUser").update(datas)
    print("6")
    
def ask(var):
    speak(var)
    st.write(var)
    question1 = record_and_transcribe()
    st.write(question1)
    question1a_output = question1a_chain.run(question1)
    st.write(question1a_output)
    addData(var, question1a_output)
           
if __name__ == "__main__":

    # L'interface utilisateur de Streamlit
    st.title("Questionnaire habitat")
    
    if st.button('Commencer le questionnaire'):
        
        
        MAX_ITERATIONS = 1
        for _ in range(MAX_ITERATIONS):
            quest = ask("Etes-vous capable de vous déplacer dans votre appartement sans crainte")
            quest = ask("Utilisez-vous un moyen auxiliaire lorsque vous vous déplacer dans votre appartement ?")
            quest = ask("La porte de votre salle de bain possède-t-elle un seuil ?")
            if quest == "Oui":
                quest = ask("Est-il difficile pour vous d’enjamber ce seuil en toute sécurité ?")
                if quest == "Oui":
                    speak("Nous vous conseillons de prendre contact avec un ergothérapeute afin que vous puissiez trouvez une solution pour vous sentir davantage en sécurité lorsque vous enjambez le seuil de votre salle de bain. Votre seuil pourrait par exemple être aplani.") 
            quest = ask("Lorsque vous êtes dans votre salle de bain, avez-vous l’impression que la luminosité est suffisante ?")
            if quest == "Non":
                speak("Nous vous conseillons d’améliorer la luminosité à l’intérieur de votre salle de bain.  Vous pourriez par exemple modifier l’ampoule de la lampe existante, ou ajouter une lampe d’appoint dans votre salle de bain")
            quest = ask("-	Arrivez-vous à allumer et à éteindre facilement la lumière de la salle de bain ?")
            if quest == "Non":
                speak("Nous vous conseillons d’installer une ampoule à détecteur de mouvement dans votre salle de bain. De telles ampoules sont disponibles par exemple à Micasa, à Jumbo, à Hornbach et à Do it + Garten et coûtent entre 15 et 20 CHFs. ")
            quest = ask("Est-il difficile pour vous de rester plus de 30 minutes debout ?")
            if quest == "Oui":
                ask("Avez-vous un endroit pour vous asseoir dans la salle de bain ?")
                if quest == "Non":
                    speak("Nous vous conseillons d’installer une chaise ou un tabouret dans votre salle de bain. Si cela n’est pas possible, nous vous conseillons de contacter un ergothérapeute afin qu’une solution puisse être trouvée avec lui.")
            quest= ask("Votre salle de bain est-elle encombrée ?")
            if quest == "Oui":
                speak("Nous vous conseillons de désencombrer votre salle de bain, c’est-à-dire d’enlever les choses superflues et de faire de l’ordre, afin optimiser la place et de pouvoir vous y déplacer plus librement.")
                

            quest= ask("Avez-vous des tapis dans votre salle de bain?")
            if quest == "Oui":

                quest= ask("Vos tapis sont-ils fixés au sol ?")
                if quest == "Non":
                    speak("Nous vous conseillons d’enlever les tapis de votre salle de bain ou de les fixer au sol.")
            quest= ask("Arrivez-vous à accéder facilement à vos affaires de toilettes à la salle de bain ?")
            if quest == "Non":
                speak("Nous vous conseillons de réorganiser les espaces de rangement de votre salle de bain afin que vous puissiez accéder plus facilement à vos affaires de toilettes, par exemple en plaçant les affaires que vous utilisez régulièrement à la hauteur de votre tronc.")
                    
            quest= ask("-	Le mobilier de votre salle de bain est-il stable ?")
            if quest == "Non":
                speak("Nous vous conseillons d’entreprendre des démarches afin que l’ensemble du mobilier de votre salle de bain soit installé de manière stable.")
            quest= ask("-	Les prises électriques de la salle de bain sont-elles en bon état (c’est-à-dire qu’elles ne sont pas endommagées) ?")
            if quest == "Non":
                speak("Nous vous conseillons de faire intervenir un électricien afin de remettre les prises électriques en bon état.")
                
                
            quest= ask("-	Les cordons électriques des appareils que vous utilisez à la salle de bain sont-ils en bon état (c’est-à-dire que le caoutchouc n’est pas endommagé) ?")
            if quest  == "Non" :
                speak("Nous vous conseillons de changer le matériel dont les cordons électriques ne sont pas en bon état.")
                
            
            quest= ask("Nous vous conseillons de changer le matériel dont les cordons électriques ne sont pas en bon état.")
            if quest == "Non":
                speak("Si votre lavabo vous semble trop haut, nous vous conseillons de prendre contact avec un ergothérapeute afin de trouver une solution pour que vous puissiez utiliser le lavabo de manière plus sécuritaire. Si votre lavabo vous semble trop bas, vous pouvez essayer d’installer une chaise devant celui-ci pour pouvoir l’utiliser en position assise. ")
            quest= ask("Avez-vous une baignoire que vous utilisez ?")
            if quest == "Oui":
                
                quest= ask("Arrivez-vous à entrer et à sortir facilement de la baignoire ?")
                if quest == "Non":
                    speak("Nous vous conseillons de contacter un ergothérapeute afin de trouver une solution pour que vous puissiez entrer et sortir plus facilement de la baignoire. Il existe différentes solutions pour cela.  ")
                quest= ask("Vous sentez-vous en sécurité lorsque vous utilisez votre baignoire ?")
                if quest =="Non":
                    speak("Nous vous conseillons de contacter un ergothérapeute afin de trouver une solution pour que vous vous sentiez davantage en sécurité lorsque vous utilisez votre baignoire. Il existe différentes solutions pour cela. Vous pourriez par exemple : ")
                    
                    
            quest= ask("Avez-vous une douche que vous utilisez ?")
            if quest =="Oui":
                ask("Arrivez-vous à entrer et à sortir facilement de la douche ?")
                if quest == "Non":
                    speak("Nous vous conseillons de contacter un ergothérapeute afin de trouver une solution pour que vous puissiez entrer et sortir plus facilement de la douche. Il existe différentes solutions pour cela. Vous pourriez par exemple : ")
                quest= ask("Vous sentez-vous en sécurité lorsque vous utilisez votre douche ?")
                if quest =="Non":
                    speak("Nous vous conseillons de contacter un ergothérapeute afin de trouver une solution pour que vous vous sentiez davantage en sécurité lorsque vous utilisez votre douche. Il existe différentes solutions pour cela. Vous pourriez par exemple : ")
                    
            quest= ask("Arrivez-vous à vous asseoir et à vous lever facilement des toilettes ?")
            if quest =="Non":
                speak("Nous vous conseillons de contacter un ergothérapeute afin de trouver une solution pour que vous puissiez vous asseoir et vous lever plus facilement des toilettes. Il existe différentes solutions pour cela. ")
                
     
          

           

            
      
