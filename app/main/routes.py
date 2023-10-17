from flask import session, redirect, url_for, render_template, request, flash

from . import main
from .forms import LoginForm
active_chat_rooms = {}
import random;
import uuid


active_rooms = {}

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
        active_rooms[room_id] = {'name': name}  # Add room to active_rooms dictionary
        session['name'] = name
        session['room_id'] = room_id
        return redirect(url_for('.chat', room_id=room_id))
    return render_template('create_room.html')


@main.route('/join_room', methods=['GET', 'POST'])
def join_room():
    if request.method == 'POST':
        name = request.form['name']
        room_id = request.form['room_id']
        if room_id not in active_rooms:
            flash('The room does not exist.', 'warning')
            return redirect(url_for('join_room'))
        session['name'] = name
        return redirect(url_for('.chat', room_id=room_id))
    return render_template('join_room.html')