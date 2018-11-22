from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String, ForeignKey, String, Column,BigInteger
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()
'''
class Station(db.Model):
    """Model for the stations table"""
    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String)
    lng = db.Column(db.Float)
    words = db.Column(postgresql.ARRAY(str))
'''
class Transcript(db.Model):
    __tablename__ = 'transcript'
    id = db.Column(db.Integer, primary_key = True)
    file_name = db.Column(db.String(200))
    transcription = db.Column(db.String)
    word_list = db.Column(ARRAY(String))

