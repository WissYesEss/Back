import os
import platform
from flask import abort, flash, redirect, render_template, request, url_for, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from werkzeug.utils import secure_filename
import requests
import re
import random
from flask import render_template
from models import Transcript
from gtts import gTTS 
from urllib import unquote
import paramiko
import datetime
import pygame 
#import pyttsx3

app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://foxevejecsahkx:ecaa3d9a25fd19a7a9da45b2de42dcb5e449c9ff3e23795b82511d17d09c060e@ec2-79-125-8-105.eu-west-1.compute.amazonaws.com:5432/dcmt3d1vec8alp'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://foxevejecsahkx:ecaa3d9a25fd19a7a9da45b2de42dcb5e449c9ff3e23795b82511d17d09c060e@localhost:5432/dcmt3d1vec8alp'
app.config['DEBUG'] = True
db.init_app(app)

@app.route('/')

def main():
    return 'Hello wissaalllll!'

@app.route('/insertText', methods=['POST' , 'GET'])

def insertText():
    if request.form:
        wordList = re.sub("[^\w]", " ",  request.form.get("text")).split();
        trans = Transcript(transcription=request.form.get("text") , word_list=wordList)
        db.session.add(trans)
        db.session.commit()
        i = 0
        returnedList = []
        data = {'words': []}
        while i < 10:
            x=random.choice(wordList)
            res = requests.get("https://dictionnaire-api.herokuapp.com/exact_def/{}".format(x)).json()
            print(x)
            if (len(res['items']) == 0) : 
                print('nexiste une def')
            else:
                i = i+1
                definition = res['items'][0]['def']
                data['words'].append({'word': x , 'definiton':definition})
                print(data)
                returnedList.append(x)
        #return render_template("words.html" , words=returnedList)
        return jsonify(data)

    return render_template("home.html" )


@app.route('/insertTrans', methods=['POST' , 'GET' ])

def insertTrans():

    if request.method == 'POST':
        print('json',request.json)
        print('getj',request.get_json('text'))
        req_data =request.get_json()
        print('text',req_data['text'])
        print('data',request.data)
        #return jsonify({'message':req_data['text']})
        #for i in request.json:
        print(request.json['text'])
                
        if request.data:
            data= req_data['text']
            
            wordList = re.sub("[^\w]", " ", request.json['text']).split()
            print('wordList',wordList)
            trans = Transcript(transcription=data , word_list=wordList)
            db.session.add(trans)
            db.session.commit()
            i = 0
            returnedList = []
            jsondata = {'words': []}
            while i < 10:
                x=random.choice(wordList)
                res = requests.get("https://dictionnaire-api.herokuapp.com/exact_def/{}".format(x)).json()
                print(x)
                if (len(res['items']) == 0) : 
                    print('nexiste une def')
                else:
                    i = i+1
                    definition = res['items'][0]['def']
                    jsondata['words'].append({'word': x , 'definiton':definition})
                    print(jsondata)
                    returnedList.append(x)
            #return render_template("words.html" , words=returnedList)
            return jsonify(jsondata)            
    else:
        return jsonify({'message':'no post'})    
        


@app.route('/definition', methods=['POST' , 'GET'])
def getting_word_def():
    if request.form:
        word=request.form.get("word")
        res = requests.get("https://dictionnaire-api.herokuapp.com/exact_def/{}".format(word)).json()
        print('test')
        return res['items'][0]['def']

@app.route('/audioTest', methods=['POST' , 'GET'])
def getting_audio_file():
    if request.method == 'POST':
        # text to speech
        mytext =request.json['question']
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False) 
        myobj.save("welcome.mp3")

        #cnx ssh
        k = paramiko.RSAKey.from_private_key_file("google_compute_engine",password='inH695Pu')
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print "connecting"
        c.connect( hostname = "35.198.131.73",username = "romain",pkey=k,look_for_keys=False)
        print "connected"
        
        #ssh_stdin, ssh_stdout, ssh_stderr = c.exec_command("cd /var/www/html/public/courses/  && ls")
        #print(ssh_stdout.readlines())

        # upload file on server
        ftp_client=c.open_sftp()
        now = datetime.datetime.now()
        name = now.isoformat()
        remote_link = 'https://courses.yesnyoulearning.com/public/courses/'+name+'.mp3'
        ftp_client.put('welcome.mp3','/var/www/html/public/courses/'+name+'.mp3')
        ftp_client.close()

        return remote_link 
    else:
        return jsonify({'message':'no post'}) 
           
if __name__ == '__main__':
    app.run()