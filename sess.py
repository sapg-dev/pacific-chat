from flask import Blueprint, render_template, request, session, redirect, url_for
from extensions import db  # Import the db instance from extensions.py
from models import Room  # Import the Room model from models.py

sess = Blueprint('sess', __name__)

@sess.route('/')
def index():
    return render_template('index.html')

@sess.route('/chat/<room_name>')
def chat(room_name):
    if 'current_room' in session:
        if session['current_room'] == room_name:
            return render_template('chat.html', room=room_name)
        else:
            return redirect(url_for('chat', room_name=session['current_room']))
    else:
        session['current_room'] = room_name
        room = Room.query.filter_by(id=room_name).first()
        if not room:
            # Handle the case where the room does not exist in the database
            # You can redirect the user or display a message
            pass
        return render_template('chat.html', room=room_name)
