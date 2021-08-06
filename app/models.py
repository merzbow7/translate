from datetime import datetime

from app import db


class Translate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    en = db.Column(db.String(25), unique=True, nullable=False)
    transcription = db.Column(db.String(25), unique=True)
    ru = db.Column(db.String(25), nullable=False)
    repeat_date = db.Column(db.Date, default=datetime.now())

    def __repr__(self):
        return f'<id {self.id}>'


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    lyrics = db.Column(db.Text)

    def __repr__(self):
        return f'<{self.title}>'


class EnglishWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=True, nullable=False)


class RussianWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=True, nullable=False)
