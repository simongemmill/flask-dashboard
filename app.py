from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
import redis
import os

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

# Load Redis URI from secret file
def load_redis_uri():
    try:
        with open("/etc/secrets/Redris.env") as f:
            return f.read().strip()
    except Exception as e:
        print("Failed to load Redis URI:", e)
        return None

redis_uri = load_redis_uri()
redis_client = redis.Redis.from_url(redis_uri) if redis_uri else None

# Example Redis usage
if redis_client:
    redis_client.set("dashboard_status", "active")
    status = redis_client.get("dashboard_status").decode("utf-8")
    print("Redis status:", status)

# Initial state
state = {
    "timeline": 0.0,
    "yen_counter": -3.0,
    "yo_counter": 0.0,
    "statoshi_balance": 1_000_000_000,
    "p_balance": 0.0,
    "ten_balance": 0.0
}

unit = 1.0

@app.route('/')
def index():
    return render_template('index.html')  # Served from /templates

def background_task():
    while True:
        # Timeline updates
        state["timeline"] += 4.0
        state["timeline"] -= 1.5
        state["timeline"] += 1.0
        for _ in range(3):
            state["timeline"] -= 0.001
        state["timeline"] += 5 * unit

        # Counter updates
        state["yen_counter"] += state["timeline"]
        state["yo_counter"] += 1_000_000 * unit

        # Balance updates
        state["p_balance"] += 9.0
        state["ten_balance"] += 9.0
        state["ten_balance"] *= 1.15

        # Emit updated state to frontend
        socketio.emit("state_update", state)

        time.sleep(1)

# Start background thread
threading.Thread(target=background_task, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)
