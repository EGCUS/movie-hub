from flask_wtf import FlaskForm
from wtforms import SubmitField


class MovieForm(FlaskForm):
    submit = SubmitField('Save movie')
