from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
import redis
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

# Load Redis URI from Render Secret File
def load_redis_uri():
    try:
        with open("/etc/secrets/redis.env") as f:
            return f.read().strip()
    except Exception as e:
        print("❌ Failed to load Redis URI:", e)
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
updatesPaused = False

@app.route("/")
def home():
    return "✅ Flask dashboard backend is running"

@app.route("/start", methods=["POST"])
def start():
    global updatesPaused
    updatesPaused = False
    return jsonify({"status": "started"})

@app.route("/pause", methods=["POST"])
def pause():
    global updatesPaused
    updatesPaused = True
    return jsonify({"status": "paused"})

@app.route("/reset", methods=["POST"])
def reset():
    state["timeline"] = 0.0
    return jsonify({"status": "reset"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "paused" if updatesPaused else "running"})

def background_task():
    while True:
        try:
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

        except Exception as e:
            print("⚠️ Background task error:", e)
            time.sleep(2)

# Start background thread
threading.Thread(target=background_task, daemon=True).start()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
