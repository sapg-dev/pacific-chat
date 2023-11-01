from flask import session, redirect, url_for, render_template, request, flash

from extensions import db   # Import db and app from chat.py
from models import Room, ChatRoom, Participant  # Import models
from . import main
from .forms import LoginForm

import random;
import uuid




@main.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        room_name = form.room.data  # Get the selected room name

        # Check if the user is already in a room with the same name
        if 'current_room' in session and session['current_room'] == room_name:
            flash('You are already in this room.', 'warning')
            return redirect(url_for('.chat', room_name=room_name))
        else:
            session['current_room'] = room_name

        # Check if the agreement checkbox is checked
     

    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')

    active_users = random.randint(1, 10)
    return render_template('index.html', form=form, active_users=active_users)




@main.route('/chat/<room_id>')
def chat(room_id):
    name = session.get('name', '')
    if not name or not room_id:
        flash('Please create a room first.', 'warning')
        return redirect(url_for('.create_room'))
    return render_template('chat.html', name=name, room_id=room_id)


@main.route('/', methods=['GET'])
def landing():
    return render_template('landing.html')






@main.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        name = request.form['name']
        room_id = str(uuid.uuid4())
        
        # Create a new room entry and add to the database
        new_room = Room(id=room_id)
        db.session.add(new_room)
        db.session.commit()

        # Create a new participant entry and add to the database
        new_participant = Participant(name=name, room_id=new_room.id)
        db.session.add(new_participant)
        db.session.commit()

        session['name'] = name
        session['room_id'] = room_id
        return redirect(url_for('.chat', room_id=room_id))
    return render_template('create_room.html')


@main.route('/join_room', methods=['GET', 'POST'])
def join_room():
    if request.method == 'POST':
        name = request.form['name']
        room_id = request.form['room_id']

        # Check if the room exists in the database
        room = Room.query.filter_by(id=room_id).first()
        if not room:
            flash('The room does not exist.', 'warning')
            return redirect(url_for('join_room'))

        # Add the user as a participant for that room
        new_participant = Participant(name=name, room_id=room.id)
        db.session.add(new_participant)
        db.session.commit()

        session['name'] = name
        return redirect(url_for('.chat', room_id=room_id))
    return render_template('join_room.html')
