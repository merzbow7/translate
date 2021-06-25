import os
from dotenv import load_dotenv
from pathlib import Path

files = list(Path(__file__).parent.glob('*.env'))
if files:
    load_dotenv(files[0])


class Configuration(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abra-cadabra-ahalay-mohalay'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

