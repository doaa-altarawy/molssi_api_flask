from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField


class LibraryForm(FlaskForm):
    name = StringField('What is your name?')
    domain = StringField('Which domain')
    submit = SubmitField('Submit')
