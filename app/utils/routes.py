from flask import Blueprint, request, redirect, url_for, render_template, current_app
from flask_socketio import emit
from utils.sockets import socketio
from tasks.scraper import GA4Scraper
from tasks.ping import Ping
import threading
import time
from datetime import datetime

b = Blueprint("routes", __name__)
worker = None
stop_event = threading.Event()
user_values = {}

# Connect after the instance is declared. 
@socketio.on("connect")
def show_connect():
    print("You are connected to socketio")
    if user_values:
        emit("user_values", user_values)

@b.route("/")
def index():
    return render_template("index.html")

@b.route("/submit", methods=["POST"])
def submit():
    global worker_thread
    account_id = request.form["ga4_account_id"]
    property_id = request.form["ga4_property_id"]
    homepage_url = request.form["website_home_page"]
    ga4_url = f"https://analytics.google.com/analytics/web/#/a{account_id}p{property_id}/reports/intelligenthome"
    stop_event.clear()

    user_values["account_id"] = account_id
    user_values["property_id"] = property_id
    user_values["homepage_url"] = homepage_url
    user_values["ga4_url"] = ga4_url

    app = current_app._get_current_object()

    def worker():
        scraper = GA4Scraper()
        scraper.connect()
        scraper.navigate(ga4_url)

        while not stop_event.is_set():
            timestamp = datetime.now().strftime("%H:%M:%S")
            result = {"Timestamp": timestamp}
            active_users = scraper.get_active_users()
            ping_time = Ping(homepage_url).run()

            if not isinstance(active_users, (int, float)) or isinstance(active_users, bool):
                active_users = "N/A"
            if not isinstance(ping_time, (int, float)) or isinstance(ping_time, bool):
                ping_time = -1  

            result["active_users"] = active_users
            result["ping"] = ping_time

            with app.app_context():
                print(result["active_users"])
                print(f"""FROM APP CONTEXT:
                Timestamp: {result['Timestamp']}
                Active Users: {result['active_users']}
                Ping: {result['ping']}
                """)
                socketio.emit("new_data", result)

            time.sleep(30)

    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()

    return redirect(url_for("routes.results"))

@b.route("/results")
def results():
    return render_template("results.html")

@socketio.on("quit")
def quit_collection(status: bool):
    pass

@socketio.on("download")
def download_data(data: list):
    pass