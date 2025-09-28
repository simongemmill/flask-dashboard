from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
import redis
import os

app = Flask(__name__)
CORS(app)  # Allow WordPress frontend to connect
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

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
updatesPaused = False  # Global control flag

@app.route('/')
def index():
    return "Backend is running"

@app.route('/start', methods=['GET'])
def start_route():
    global updatesPaused
    updatesPaused = False
    return "Updates resumed"

@app.route('/pause', methods=['GET'])
def pause_route():
    global updatesPaused
    updatesPaused = True
    return "Updates paused"

@app.route('/reset', methods=['GET'])
def reset_route():
    state["timeline"] = 0.0
    return "Timeline reset"

def background_task():
    while True:
        if not updatesPaused:
            # Timeline logic
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

            # Emit to frontend
            socketio.emit("state_update", state)

            # Save to Redis
            if redis_client:
                redis_client.set("latest_timeline", state["timeline"])

        time.sleep(1)

# Start background thread
threading.Thread(target=background_task, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, host='3.134.238.10', port=32)

