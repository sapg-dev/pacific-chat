from flask import Flask
from app import create_app, socketio
from extensions import db
from sess import sess


app = create_app(debug=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatrooms.db'
db.init_app(app)
app.register_blueprint(sess)


@app.cli.command("create-db")
def create_db():
    """Create the db tables."""
    db.create_all()
    print("Database tables created.")



if __name__ == '__main__':
    socketio.run(app)