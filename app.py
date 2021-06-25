from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
