from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dictionary to store active chat rooms and their participants
active_rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat/<room_name>')
def chat(room_name):
    if 'current_room' in session:
        if session['current_room'] == room_name:
            return render_template('chat.html', room=room_name)
        else:
            return redirect(url_for('chat', room_name=session['current_room']))
    else:
        session['current_room'] = room_name
        if room_name not in active_rooms:
            active_rooms[room_name] = set()
        return render_template('chat.html', room=room_name)

if __name__ == '__main__':
    app.run(debug=True)
