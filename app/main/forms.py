from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms import StringField, SelectField    

class LoginForm(FlaskForm):
    """Accepts a nickname and a room."""
    name = StringField('username', validators=[DataRequired()])
    room_choices = [('Room', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3')]  # Replace with your desired choices

    room = SelectField('Room', choices=room_choices, validators=[DataRequired()])


    agree_to_terms = BooleanField('I agree to the terms and conditions', validators=[DataRequired()])
    
    submit = SubmitField('Enter Chatroom')



