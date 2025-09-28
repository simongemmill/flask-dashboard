from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
import redis

# Connect to Redis using your URI
redis_client = redis.Redis.from_url("redis://red-d3cfita4d50c73cgu7kg:6379")

# Example usage
redis_client.set("dashboard_status", "active")
status = redis_client.get("dashboard_status").decode("utf-8")
print("Redis status:", status)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

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

def index():
    return render_template('index.html')  # Make sure this file is in /templates

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

    socketio.run(app, host='127.0.0.1', port=32, debug=True)

