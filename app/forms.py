from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, DateTimeLocalField
from wtforms.validators import DataRequired, URL

class HostLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
    
class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    event_datetime = DateTimeLocalField("Event Time",format="%Y-%m-%dT%H:%M",validators=[DataRequired()])
    host = StringField("Host", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Save")

class ResourceForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Save")
