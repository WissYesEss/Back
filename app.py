import os
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
        while i < 10:
            x=random.choice(wordList)
            i = i +1
            returnedList.append(x)
        return render_template("words.html" , words=returnedList)

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
            
            return jsonify({'message':'success story'})
    else:
        return jsonify({'message':'no post'})    
        


@app.route('/definition', methods=['POST' , 'GET'])
def getting_word_def():
    if request.form:
        word=request.form.get("word")
        res = requests.get("https://dictionnaire-api.herokuapp.com/exact_def/{}".format(word)).json()
        print('test')
        return res['items'][0]['def']


if __name__ == '__main__':
    app.run()