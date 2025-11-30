from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    host = StringField("Host", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Save")
