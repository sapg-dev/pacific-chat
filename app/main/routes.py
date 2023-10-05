from flask import session, redirect, url_for, render_template, request, flash

from . import main
from .forms import LoginForm
active_chat_rooms = {}
import random;
@main.route('/', methods=['GET', 'POST'])
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
        if form.agree_to_terms.data:
            return redirect(url_for('.chat', room_name=room_name))
        else:
            flash('Please agree to the terms and conditions.', 'warning')

    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')

    active_users = random.randint(1, 10)
    return render_template('index.html', form=form, active_users=active_users)




@main.route('/chat/<room_name>')
def chat(room_name):
    name = session.get('name', '')
    current_room = session.get('current_room', '')

    if name == '' or room_name == '':
        return redirect(url_for('.index'))

    if current_room != room_name:
        flash('You are not authorized to enter this room.', 'danger')
        return redirect(url_for('.index'))

    return render_template('chat.html', name=name, room=room_name)



