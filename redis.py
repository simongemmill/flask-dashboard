import os
import redis

# Safely load Redis URL from environment variable
redis_url = os.environ.get("REDIS_URL")

# Connect to Redis
r = redis.from_url(redis_url)

# Set and retrieve a test value
r.set("key", "redis-py")
print(r.get("key").decode())
