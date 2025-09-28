import os
import redis

# Connect to your Key Value instance using the REDIS_URL environment variable
# The REDIS_URL is set to the internal connection URL e.g. redis://red-343245ndffg023:6379
r = redis.from_url(os.environ['rediss://red-d3cfita4d50c73cgu7kg:fd5oeGXHR8AcGIbJBwkIC9S4wXET3kRJ@oregon-keyvalue.render.com:6379'])

# Set and retrieve some values
r.set('key', 'redis-py')

print(r.get('key').decode())
