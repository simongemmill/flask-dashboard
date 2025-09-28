import os
import redis

# Connect to your Key Value instance using the REDIS_URL environment variable
# The REDIS_URL is set to the internal connection URL e.g. redis://red-343245ndffg023:6379
r = redis.from_url(os.environ['REDIS_URL'])

# Set and retrieve some values
r.set('key', 'redis-py')
print(r.get('key').decode())