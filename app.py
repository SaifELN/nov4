from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*")

db_path = os.path.join(os.path.dirname(__file__), 'chat.db')

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user TEXT NOT NULL,
                  message TEXT NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    user = data['user']
    message = data['message']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO messages (user, message) VALUES (?, ?)", (user, message))
    conn.commit()
    conn.close()

    emit('new_message', {'user': user, 'message': message, 'timestamp': timestamp}, broadcast=True)

@app.route('/get_messages')
def get_messages():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT user, message, timestamp FROM messages ORDER BY timestamp DESC LIMIT 50")
    messages = [{'user': row[0], 'message': row[1], 'timestamp': row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(messages)

if __name__ == '__main__':
    init_db()
    app.run()  # Remove socketio.run() and use app.run() instead
