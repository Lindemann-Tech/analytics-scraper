from flask import Flask
from flask_socketio import SocketIO
from utils.routes import b
from utils.sockets import socketio
import threading
import time
import os
import subprocess

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))
socketio.init_app(app, cors_allowed_origins="*")
app.register_blueprint(b)

def open_browser():
    time.sleep(2)
    subprocess.Popen([
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "--remote-debugging-port=9222",
        "--user-data-dir=C:/AutomationProfile",
        "http://127.0.0.1:5000"      
    ])

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    socketio.run(app, debug=True, use_reloader=False)