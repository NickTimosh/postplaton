from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import DateField

class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    host = StringField("Host", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Save")
