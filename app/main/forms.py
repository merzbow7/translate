from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class URLForm(FlaskForm):
    url = StringField("Адрес:", validators=[DataRequired(message="Введите адрес!")])
